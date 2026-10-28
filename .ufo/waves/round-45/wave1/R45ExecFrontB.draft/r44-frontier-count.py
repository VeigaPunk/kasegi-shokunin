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

    Round 45 (routed defect R3) turns the probe into a gate: `--selftest`
    builds isolated README fixtures, grades each case on exit code AND the
    exact printed line, then replays the same cases against mutated in-memory
    variants of the counting function and requires every mutant to be
    rejected.  A selftest that cannot fail is not evidence.

USAGE
    python3 corpus/instruments/r44-frontier-count.py --root TREE [--expect N] [--ids]
    python3 corpus/instruments/r44-frontier-count.py --selftest [--work DIR]

    --root      tree to count (an exported lane tree, or the lane checkout)
    --expect    when given, the counted value must equal it, else exit 1
    --ids       also print the counted row ids
    --selftest  run the graded fixture cases and the mutant check; --root is
                not required.  Exit 0 only when failures=0.
    --work      selftest scratch parent (default: a fresh temp directory);
                only the subdirectory the selftest creates is removed.

OUTPUT
    frontier rows=<n> admitted=<k>
    frontier duplicate-ids=<ids> verdict=DEFECT exit=1
    frontier expected=<N> admitted=<k> verdict=SHORT exit=1
    selftest: ... mutants=<k> rejected=<k> then `selftest cases=<N> failures=<F>` last
"""

from __future__ import annotations

import argparse
import contextlib
import inspect
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROW_RX = re.compile(r"^\| F\d+ \|")


def count_frontier(root: str) -> tuple[int, int, list[str]]:
    readme = os.path.join(root, "corpus", "README.md")
    rows = 0
    admitted = 0
    ids: list[str] = []
    try:
        with open(readme, "r", encoding="utf-8") as fh:
            for line in fh:
                if not ROW_RX.match(line):
                    continue
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) < 3:
                    continue
                rows += 1
                ids.append(cells[0])
                if cells[2] == "admitted":
                    admitted += 1
    except OSError as exc:
        print(f"r44-frontier-count: cannot read {readme}: {exc}", file=sys.stderr)
        return 0, 0, []
    return rows, admitted, ids


def run_count(args_root: str, expect: int | None, show_ids: bool, counter) -> int:
    if not os.path.isdir(args_root):
        print(f"r44-frontier-count: root {args_root} is not a directory", file=sys.stderr)
        return 2

    rows, admitted, ids = counter(args_root)
    if show_ids:
        print("frontier-ids=" + ",".join(ids))
    # R44W2Rev10 false-pass shape: a duplicated frontier row would inflate the
    # admitted count without adding a distinct holding. Duplicate ids are a
    # defect, never a pass.
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        print(f"frontier duplicate-ids={','.join(dupes)} verdict=DEFECT exit=1")
        return 1
    print(f"frontier rows={rows} admitted={admitted}")
    if expect is not None and admitted != expect:
        print(f"frontier expected={expect} admitted={admitted} verdict=SHORT exit=1")
        return 1
    return 0


# ----------------------------------------------------------------------------
# selftest
# ----------------------------------------------------------------------------

README_HEAD = (
    "# corpus\n\n"
    "| source | tier | status |\n|---|---|---|\n"
    "| S001 | A | admitted |\n| S002 | B | admitted |\n\n"
    "## Frontier\n\n"
    "| id | topic | status | entry | sources | next |\n"
    "|---|---|---|---|---|---|\n"
)


def frow(n: int, status: str = "admitted", title: str | None = None) -> str:
    t = title if title is not None else f"topic {n}"
    return f"| F{n:02d} | {t} | {status} | knowledge/k{n}.md | S{n:03d} | next {n}. |\n"


def readme(rows: list[str], tail: str = "\n## Notes\n\nprose, not a table.\n") -> str:
    return README_HEAD + "".join(rows) + tail


def build_fixtures(work: str) -> dict[str, str]:
    """Write one fixture tree per scenario under `work`; return name -> root."""
    spec: dict[str, str | None] = {
        "n26": readme([frow(i) for i in range(1, 27)]),
        "n27": readme([frow(i) for i in range(1, 28)]),
        "dup": readme([frow(i) for i in range(1, 27)] + [frow(5)]),
        "queued": readme([frow(i) for i in range(1, 26)] + [frow(26, "queued")]),
        # status in the SECOND cell: the shape the dead round-44 frozen regex assumed.
        "second": readme([frow(i) for i in range(1, 26)]
                         + ["| F26 | admitted | topic 26 | knowledge/k26.md | S026 | next. |\n"]),
        "notadm": readme([frow(i) for i in range(1, 26)] + [frow(26, "not admitted")]),
        # table header and separator only: zero rows (the S table above has `admitted` cells
        # and must never be counted either).
        "headeronly": README_HEAD + "\n## Notes\n",
        # last row without a trailing newline still counts
        "nonl": readme([frow(i) for i in range(1, 26)]).rstrip("\n")
                + "\n| F26 | topic 26 | admitted | knowledge/k26.md | S026 | next. |",
        "norm": None,  # no corpus/README.md at all
    }
    roots: dict[str, str] = {}
    for name, text in spec.items():
        root = os.path.join(work, name)
        os.makedirs(os.path.join(root, "corpus"))
        if text is not None:
            with open(os.path.join(root, "corpus", "README.md"), "w", encoding="utf-8") as fh:
                fh.write(text)
        roots[name] = root
    roots["noroot"] = os.path.join(work, "does-not-exist")
    return roots


# (case name, fixture, extra argv, expected rc, expected stdout exactly)
CASES: list[tuple[str, str, list[str], int, str]] = [
    ("26-rows-26-admitted", "n26", [], 0, "frontier rows=26 admitted=26\n"),
    ("27th-admitted-row-counts-27", "n27", [], 0, "frontier rows=27 admitted=27\n"),
    ("expect-27-on-27-exits-0", "n27", ["--expect", "27"], 0, "frontier rows=27 admitted=27\n"),
    ("expect-27-on-26-is-SHORT", "n26", ["--expect", "27"], 1,
     "frontier rows=26 admitted=26\nfrontier expected=27 admitted=26 verdict=SHORT exit=1\n"),
    ("duplicate-F-id-is-DEFECT", "dup", [], 1,
     "frontier duplicate-ids=F05 verdict=DEFECT exit=1\n"),
    ("duplicate-id-beats-expect", "dup", ["--expect", "27"], 1,
     "frontier duplicate-ids=F05 verdict=DEFECT exit=1\n"),
    ("queued-row-is-row-not-admitted", "queued", [], 0, "frontier rows=26 admitted=25\n"),
    ("header-and-separator-not-counted", "headeronly", [], 0, "frontier rows=0 admitted=0\n"),
    ("status-in-second-cell-not-admitted", "second", [], 0, "frontier rows=26 admitted=25\n"),
    ("not-admitted-is-not-admitted", "notadm", [], 0, "frontier rows=26 admitted=25\n"),
    ("last-row-without-newline-counts", "nonl", [], 0, "frontier rows=26 admitted=26\n"),
    ("--ids-prints-ids-first", "n26", ["--ids"], 0,
     "frontier-ids=" + ",".join(f"F{i:02d}" for i in range(1, 27))
     + "\nfrontier rows=26 admitted=26\n"),
    ("missing-README-is-zero-rows-exit-0", "norm", [], 0, "frontier rows=0 admitted=0\n"),
    ("missing-root-exits-2", "noroot", [], 2, ""),
]

# (mutant name, exact source text in count_frontier, replacement)
MUTANTS: list[tuple[str, str, str]] = [
    ("status-compared-to-queued", 'cells[2] == "admitted"', 'cells[2] == "queued"'),
    ("status-read-from-second-cell", 'cells[2] == "admitted"', 'cells[1] == "admitted"'),
    ("status-substring-match", 'cells[2] == "admitted"', '"admitted" in cells[2]'),
    ("every-row-admitted", 'if cells[2] == "admitted":', "if True:"),
    ("any-pipe-line-is-a-row", "ROW_RX.match(line)", 're.match(r"^\\|", line)'),
    ("ids-not-collected", "ids.append(cells[0])", "pass"),
]


def build_mutant(old: str, new: str):
    src = inspect.getsource(count_frontier)
    if old not in src:
        raise SystemExit(f"selftest: mutant anchor {old!r} not found in count_frontier")
    ns = {"os": os, "re": re, "sys": sys, "ROW_RX": ROW_RX}
    exec(compile(src.replace(old, new, 1), "<mutant>", "exec"), ns)  # noqa: S102
    return ns["count_frontier"]


def grade(roots: dict[str, str], counter, verbose: bool) -> int:
    """Run every CASE in-process against `counter`; return number of failing cases."""
    failures = 0
    for name, fx, extra, want_rc, want_out in CASES:
        argv = ["--root", roots[fx]] + extra
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = cli(argv, counter)
        ok = rc == want_rc and out.getvalue() == want_out
        if name == "missing-README-is-zero-rows-exit-0":
            ok = ok and "cannot read" in err.getvalue()
        if name == "missing-root-exits-2":
            ok = ok and "is not a directory" in err.getvalue()
        if not ok:
            failures += 1
        if verbose:
            print(f"case {name}: {'ok' if ok else 'FAIL'} rc={rc} out={out.getvalue()!r}"
                  + ("" if ok else f" want rc={want_rc} out={want_out!r}"))
    return failures


def subprocess_case(roots: dict[str, str]) -> tuple[bool, str]:
    """One real-CLI case: separate process, real counter, real exit code."""
    p = subprocess.run(
        [sys.executable, os.path.abspath(__file__), "--root", roots["n26"], "--expect", "27"],
        capture_output=True, text=True,
    )
    want = "frontier rows=26 admitted=26\nfrontier expected=27 admitted=26 verdict=SHORT exit=1\n"
    return p.returncode == 1 and p.stdout == want, f"rc={p.returncode} out={p.stdout!r}"


def selftest(work: str | None) -> int:
    parent = work if work else tempfile.mkdtemp(prefix="r44fc-selftest-")
    os.makedirs(parent, exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="r44fc-", dir=parent)
    try:
        roots = build_fixtures(scratch)
        total = len(CASES) + 1
        failures = grade(roots, count_frontier, verbose=True)
        ok, detail = subprocess_case(roots)
        print(f"case subprocess-cli-expect-27-on-26: {'ok' if ok else 'FAIL'} {detail}")
        failures += 0 if ok else 1

        rejected = 0
        for mname, old, new in MUTANTS:
            bad = grade(roots, build_mutant(old, new), verbose=False)
            print(f"mutant {mname}: {'rejected' if bad else 'SURVIVED'} failing-cases={bad}")
            rejected += 1 if bad else 0
        print(f"mutants={len(MUTANTS)} rejected={rejected}")
        failures += len(MUTANTS) - rejected

        print(f"selftest cases={total + len(MUTANTS)} failures={failures}")
        return 0 if failures == 0 else 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
        if not work:
            shutil.rmtree(parent, ignore_errors=True)


def cli(argv: list[str], counter=count_frontier) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root")
    ap.add_argument("--expect", type=int, default=None)
    ap.add_argument("--ids", action="store_true", help="also print the counted row ids")
    ap.add_argument("--selftest", action="store_true", help="run the graded fixture and mutant selftest")
    ap.add_argument("--work", default=None, help="selftest scratch parent directory")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest(args.work)
    if args.root is None:
        ap.error("the following arguments are required: --root")
    return run_count(args.root, args.expect, args.ids, counter)


def main(argv: list[str]) -> int:
    return cli(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
