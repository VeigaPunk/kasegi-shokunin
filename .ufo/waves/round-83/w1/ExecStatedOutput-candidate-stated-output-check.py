#!/usr/bin/env python3
"""stated-output-check.py — check the output a markdown entry says a command produced.

What it checks
--------------
A knowledge entry can assert what a command printed and what status it returned. In
the canonical shape

    `<command>` prints <output> and exits <N>

this instrument runs <command> with `bash -c` in --root (default: the current
directory) and asserts:

  * the exit status equals N;
  * when <output> is the word `nothing`, stdout is empty (stderr is ignored and only
    counted, so the omission is visible as err_lines=);
  * otherwise <output> carries exactly one backticked literal and at least one stdout
    line starts with that literal; when the phrase says "one ... line", stdout has
    exactly one line.

Commands outside that shape are not matched and not executed: a prose sentence is not
a checkable claim. The round-82 wave script (`.ufo/waves/round-82/l1/stated-output-
check.py`) matched only "prints nothing and exits 1"; this instrument keeps that limb
and adds the stated-literal and one-line limbs, which is the shape the round-82 landed
entry uses at its Limits line ("prints that one navigation line (`7:`) and exits 0").

Refusal rules (fail-closed, no execution)
-----------------------------------------
A matched command is refused, never run, when

  * a segment (split at `|`, `||`, `&&`, `;` outside quotes) does not open with an
    allow-listed head: grep egrep fgrep printf echo true false test [ wc sha256sum
    diff sort cut head tail cat ls;
  * a `python3` segment does not immediately name `corpus/instruments/<name>.py`;
  * the text carries `$(` anywhere, or `>` or a lone `&` outside quotes.

A refused command counts as a failure of the entry's stated output (the entry stated
a checkable output for a command this instrument will not run), so the exit is
fail-closed rather than silently green.

Limits — stated, not assumed
----------------------------
* NOT a sandbox. The allow-list refuses destructive heads; it is not a capability
  proof, and the entry text is trusted input. An allow-listed head can still be
  harmful in some forms.
* The environment is inherited, so command behaviour (locale, PATH) is this host's,
  not the author's. A stated output observed on another host or from another tree is
  checked against these bytes and this environment.
* "prints nothing" is a stdout claim only: a command that writes to stderr and exits N
  passes. The per-command line prints err_lines= so that omission stays visible.
* A file with no matched command passes vacuously (`commands=0`); read the count. The
  instrument cannot tell whether the stated output is the one the author actually saw,
  only whether this tree reproduces it now.
* A command slower than --timeout is a failure (`timeout`), never a pass. Only the
  first 100 characters of a command are printed.
* <output> must be quoted in backticks or be the word `nothing`; a phrase with two
  backticked literals is ambiguous and is not matched.

Exit codes: 0 every matched stated output holds and nothing was refused; 1 a mismatch
or a refusal; 2 usage or read error (missing file, non-directory --root; --selftest
also exits 2 when TMPDIR is set to a path that is not an existing directory).

Scratch: every temporary path comes from tempfile with an explicit TMPDIR base and is
removed before exit; no temporary path is hard-coded.

Usage:
  stated-output-check.py [--root DIR] [--timeout S] FILE [FILE ...]
  stated-output-check.py --selftest
"""

import argparse
import contextlib
import hashlib
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile


PAT = re.compile(
    r"`(?P<cmd>[^`\n]+)`[ \t]+prints[ \t]+"
    r"(?P<what>nothing|(?P<pre>[^`\n]*?)`(?P<lit>[^`\n]+)`[^`\n]*?)"
    r"[ \t]+and[ \t]+exits[ \t]+(?P<rc>\d+)"
)
ONE_LINE = re.compile(r"\bone\b[^.;`]{0,40}\blines?\b", re.IGNORECASE)
ASSIGN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
PY_INSTRUMENT = re.compile(r"^corpus/instruments/[A-Za-z0-9._-]+\.py$")

ALLOWED_HEADS = frozenset({
    "grep", "egrep", "fgrep", "printf", "echo", "true", "false", "test", "[",
    "wc", "sha256sum", "diff", "sort", "cut", "head", "tail", "cat", "ls",
})


class UsageError(Exception):
    """A read-side failure that maps to exit 2."""


def scratch_dir():
    """Create a scratch directory under TMPDIR (asserted) or the tempfile default."""
    base = os.environ.get("TMPDIR") or None
    if base is not None and not os.path.isdir(base):
        sys.stderr.write(
            "stated-output-check: TMPDIR is not an existing directory: %s\n" % base)
        raise SystemExit(2)
    return tempfile.mkdtemp(prefix="stated-output-check-", dir=base)


def self_sha256():
    try:
        with open(__file__, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return "unavailable"


def unsafe_text(cmd):
    """Return a refusal reason for text that can write or substitute, else None."""
    if "$(" in cmd:
        return "substitution"
    quote = None
    i = 0
    while i < len(cmd):
        ch = cmd[i]
        if quote:
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in "'\"":
            quote = ch
            i += 1
            continue
        if ch == ">":
            return "redirect"
        if ch == "&" and not cmd.startswith("&&", i):
            return "background"
        if ch == "\n":
            return "newline"
        i += 1
    return None


def split_segments(cmd):
    """Split at unquoted |, ||, && and ; into command segments."""
    segs = []
    buf = []
    quote = None
    i = 0
    while i < len(cmd):
        ch = cmd[i]
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in "'\"":
            quote = ch
            buf.append(ch)
            i += 1
            continue
        if ch == "|":
            segs.append("".join(buf))
            buf = []
            i += 2 if cmd.startswith("||", i) else 1
            continue
        if cmd.startswith("&&", i):
            segs.append("".join(buf))
            buf = []
            i += 2
            continue
        if ch == ";":
            segs.append("".join(buf))
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    segs.append("".join(buf))
    return [seg.strip() for seg in segs if seg.strip()]


def head_tokens(seg):
    """Segment tokens with leading VAR=value assignments removed."""
    toks = seg.split()
    i = 0
    while i < len(toks) and ASSIGN.match(toks[i]):
        i += 1
    return toks[i:]


def refusal(cmd):
    """Return why this command will not be executed, or None to allow it."""
    why = unsafe_text(cmd)
    if why is not None:
        return why
    for seg in split_segments(cmd):
        rest = head_tokens(seg)
        if not rest:
            return "empty-segment"
        head = rest[0]
        if head == "python3":
            args = [t for t in rest[1:] if not t.startswith("-")]
            if not args or PY_INSTRUMENT.match(args[0]) is None:
                return "python3-not-instrument"
            continue
        if head not in ALLOWED_HEADS:
            return "head-not-allowed:%s" % head
    return None


def scan(text):
    """Return the stated-output claims a text makes, in file order."""
    specs = []
    for m in PAT.finditer(text):
        what = m.group("what")
        specs.append({
            "cmd": m.group("cmd"),
            "rc": int(m.group("rc")),
            "kind": "nothing" if what == "nothing" else "literal",
            "lit": m.group("lit"),
            "want_lines": 1 if ONE_LINE.search(what) else None,
        })
    return specs


def run_command(cmd, root, timeout):
    """Run one command; return (rc, stdout, stderr, timed_out)."""
    try:
        p = subprocess.run(["bash", "-c", cmd], cwd=root, capture_output=True,
                           text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr, False
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout or ""
        if isinstance(out, bytes):
            out = out.decode("utf-8", "replace")
        return -1, out, "", True


def evaluate(spec, out, rc, timed_out):
    """Return the failure reason for one executed command, or None."""
    if timed_out:
        return "timeout"
    if rc != spec["rc"]:
        return "rc-want-%d-got-%d" % (spec["rc"], rc)
    if spec["kind"] == "nothing":
        return None if out == "" else "stdout-not-empty"
    lines = out.splitlines()
    if spec["want_lines"] is not None and len(lines) != spec["want_lines"]:
        return "one-line-want-%d-got-%d" % (spec["want_lines"], len(lines))
    if not any(line.startswith(spec["lit"]) for line in lines):
        return "literal-missing:%s" % spec["lit"]
    return None


def read_entry(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError as exc:
        raise UsageError("%s: %s" % (path, exc))


def check_text(text, root, timeout):
    """Return one row per matched command: reason is None when the claim holds."""
    rows = []
    for spec in scan(text):
        why = refusal(spec["cmd"])
        if why is not None:
            rows.append({"cmd": spec["cmd"], "reason": "refused:" + why,
                         "rc": None, "out_lines": 0, "err_lines": 0})
            continue
        rc, out, err, timed_out = run_command(spec["cmd"], root, timeout)
        rows.append({
            "cmd": spec["cmd"],
            "reason": evaluate(spec, out, rc, timed_out),
            "rc": rc,
            "out_lines": len(out.splitlines()),
            "err_lines": len(err.splitlines()),
        })
    return rows


def verdict(rows):
    """0 when every matched stated output holds and nothing was refused."""
    return 0 if all(row["reason"] is None for row in rows) else 1


def report(path, rows):
    mismatches = sum(1 for r in rows
                     if r["reason"] and not r["reason"].startswith("refused:"))
    refused = sum(1 for r in rows
                  if (r["reason"] or "").startswith("refused:"))
    print("FILE %s commands=%d mismatches=%d refused=%d"
          % (path, len(rows), mismatches, refused))
    for r in rows:
        if not r["reason"]:
            tag = "OK"
        elif r["reason"].startswith("refused:"):
            tag = "REFUSED"
        else:
            tag = "FAIL"
        rc = "-" if r["rc"] is None else str(r["rc"])
        print("%-7s rc=%s out_lines=%d err_lines=%d %s :: %s"
              % (tag, rc, r["out_lines"], r["err_lines"], r["reason"] or "",
                 r["cmd"][:100]))
    return mismatches, refused


def selftest():
    made = []
    cases = 0
    failures = 0

    def check(name, ok, detail=""):
        nonlocal cases, failures
        cases += 1
        if ok:
            print("ok   %s" % name)
        else:
            failures += 1
            print("FAIL %s%s" % (name, (": " + detail) if detail else ""))

    def world():
        d = scratch_dir()
        made.append(d)
        return d

    def put(d, name, body):
        path = os.path.join(d, name)
        os.makedirs(os.path.dirname(path) or d, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body)
        return path

    def save_tmpdir():
        return os.environ.get("TMPDIR")

    def restore_tmpdir(old):
        if old is None:
            os.environ.pop("TMPDIR", None)
        else:
            os.environ["TMPDIR"] = old

    try:
        d = world()
        put(d, "hay.txt", "needle\n")

        rows = check_text(
            "- `grep -q -F absent hay.txt` prints nothing and exits 1.\n", d, 5)
        check("pass-nothing", len(rows) == 1 and rows[0]["reason"] is None
              and verdict(rows) == 0, repr(rows))

        rows = check_text(
            "- `grep -F needle hay.txt` prints nothing and exits 0.\n", d, 5)
        check("fail-stdout-not-empty",
              len(rows) == 1 and rows[0]["reason"] == "stdout-not-empty"
              and verdict(rows) == 1, repr(rows))

        rows = check_text(
            "- `grep -q -F needle hay.txt` prints nothing and exits 1.\n", d, 5)
        check("fail-rc-want-1-got-0",
              len(rows) == 1 and rows[0]["reason"] == "rc-want-1-got-0"
              and verdict(rows) == 1, repr(rows))

        rows = check_text(
            "- `grep -n -F needle hay.txt` prints that one line (`1:`) and "
            "exits 0.\n", d, 5)
        check("pass-literal-one-line",
              len(rows) == 1 and rows[0]["reason"] is None and verdict(rows) == 0,
              repr(rows))

        rows = check_text(
            "- `grep -n -F needle hay.txt` prints that one line (`2:`) and "
            "exits 0.\n", d, 5)
        check("fail-literal-missing",
              len(rows) == 1 and rows[0]["reason"] == "literal-missing:2:",
              repr(rows))

        rows = check_text(
            "- `printf '1:a\\n1:b\\n'` prints that one line (`1:`) and exits 0.\n",
            d, 5)
        check("fail-one-line-limb",
              len(rows) == 1 and rows[0]["reason"] == "one-line-want-1-got-2",
              repr(rows))

        rows = check_text("- `rm -rf hay.txt` prints nothing and exits 0.\n", d, 5)
        check("refuse-destructive-head",
              len(rows) == 1
              and rows[0]["reason"] == "refused:head-not-allowed:rm"
              and os.path.exists(os.path.join(d, "hay.txt"))
              and verdict(rows) == 1, repr(rows))

        rows = check_text(
            "- `grep -F needle hay.txt > out.txt` prints nothing and exits 1.\n",
            d, 5)
        check("refuse-redirect",
              len(rows) == 1 and rows[0]["reason"] == "refused:redirect"
              and not os.path.exists(os.path.join(d, "out.txt")), repr(rows))

        rows = check_text(
            "- `grep -F needle hay.txt | sh` prints nothing and exits 0.\n", d, 5)
        check("refuse-second-segment-head",
              len(rows) == 1
              and rows[0]["reason"] == "refused:head-not-allowed:sh", repr(rows))

        rows = check_text(
            "- `python3 -c 'print(1)'` prints nothing and exits 1.\n", d, 5)
        check("refuse-python3-not-instrument",
              len(rows) == 1
              and rows[0]["reason"] == "refused:python3-not-instrument",
              repr(rows))

        d2 = world()
        put(d2, "corpus/instruments/probe.py", "import sys\nsys.exit(1)\n")
        rows = check_text(
            "- `python3 corpus/instruments/probe.py` prints nothing and exits "
            "1.\n", d2, 5)
        check("pass-python3-instrument",
              len(rows) == 1 and rows[0]["reason"] is None and verdict(rows) == 0,
              repr(rows))

        d3 = world()
        put(d3, "hay2.txt", "other\n")
        rows = check_text(
            "- `grep -E 'needle|absent' hay2.txt` prints nothing and exits 1.\n",
            d3, 5)
        check("quoted-pipe-not-a-segment",
              len(rows) == 1 and rows[0]["reason"] is None, repr(rows))

        rows = check_text(
            "- `grep -q -F absent hay.txt` prints nothing and exits 1.\n"
            "- `grep -F needle hay.txt` prints nothing and exits 0.\n", d, 5)
        check("multi-two-commands",
              len(rows) == 2
              and [r["reason"] for r in rows] == [None, "stdout-not-empty"]
              and verdict(rows) == 1, repr(rows))

        rows = check_text(
            "- `grep -q x hay.txt` printed nothing, exit 1.\n", d, 5)
        check("outside-grammar-not-run", rows == [] and verdict(rows) == 0,
              repr(rows))

        d4 = world()
        put(d4, "corpus/instruments/slow.py", "import time\ntime.sleep(2)\n")
        rows = check_text(
            "- `python3 corpus/instruments/slow.py` prints nothing and exits "
            "0.\n", d4, 0.3)
        check("timeout-is-a-failure",
              len(rows) == 1 and rows[0]["reason"] == "timeout"
              and verdict(rows) == 1, repr(rows))

        d5 = world()
        old = save_tmpdir()
        os.environ["TMPDIR"] = d5
        try:
            p = scratch_dir()
            made.append(p)
            honoured = os.path.realpath(p).startswith(
                os.path.realpath(d5) + os.sep)
        finally:
            restore_tmpdir(old)
        check("tmpdir-honoured", honoured, p)

        old = save_tmpdir()
        os.environ["TMPDIR"] = os.path.join(d5, "absent")
        code = None
        try:
            scratch_dir()
        except SystemExit as exc:
            code = exc.code
        finally:
            restore_tmpdir(old)
        check("tmpdir-refusal-exit-2", code == 2, "code=%r" % (code,))

        with open(__file__, encoding="utf-8") as fh:
            src = fh.read()
        check("no-hardcoded-temp-path", ("/" + "tmp") not in src)

        rc = main(["--root", d, os.path.join(d, "missing.md")])
        check("missing-file-exit-2", rc == 2, "rc=%r" % (rc,))

        rc = main(["--root", d])
        check("no-files-exit-2", rc == 2, "rc=%r" % (rc,))

        passp = put(d, "pass-entry.md",
                    "- `grep -q -F absent hay.txt` prints nothing and exits 1.\n")
        failp = put(d, "fail-entry.md",
                    "- `grep -F needle hay.txt` prints nothing and exits 0.\n")
        buf_pass = io.StringIO()
        buf_fail = io.StringIO()
        with contextlib.redirect_stdout(buf_pass):
            rc_pass = main(["--root", d, passp])
        with contextlib.redirect_stdout(buf_fail):
            rc_fail = main(["--root", d, failp])
        check("cli-exit-map",
              rc_pass == 0 and rc_fail == 1
              and "STATED-OUTPUT files=1 commands=1 mismatches=0 refused=0"
              in buf_pass.getvalue()
              and "STATED-OUTPUT files=1 commands=1 mismatches=1 refused=0"
              in buf_fail.getvalue(),
              "rc_pass=%r rc_fail=%r" % (rc_pass, rc_fail))
    finally:
        for d in made:
            shutil.rmtree(d, ignore_errors=True)

    print("selftest cases=%d failures=%d" % (cases, failures))
    return 0 if failures == 0 else 1


def main(argv):
    ap = argparse.ArgumentParser(
        prog="stated-output-check.py",
        description="Run the commands a markdown entry says print X and exit N.")
    ap.add_argument("files", nargs="*")
    ap.add_argument("--root", default=".",
                    help="directory the commands run in (default: cwd)")
    ap.add_argument("--timeout", type=float, default=60.0)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        if args.files:
            sys.stderr.write(
                "stated-output-check: --selftest takes no file arguments\n")
            return 2
        return selftest()
    if not args.files:
        ap.print_usage(sys.stderr)
        return 2
    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        sys.stderr.write(
            "stated-output-check: --root is not a directory: %s\n" % root)
        return 2
    texts = []
    for path in args.files:
        try:
            texts.append((path, read_entry(path)))
        except UsageError as exc:
            sys.stderr.write("stated-output-check: %s\n" % exc)
            return 2

    print("stated-output-check.py sha256=%s root=%s" % (self_sha256(), root))
    commands = mismatches = refused = 0
    for path, text in texts:
        rows = check_text(text, root, args.timeout)
        m, r = report(path, rows)
        commands += len(rows)
        mismatches += m
        refused += r
    print("STATED-OUTPUT files=%d commands=%d mismatches=%d refused=%d"
          % (len(texts), commands, mismatches, refused))
    return 0 if mismatches == 0 and refused == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
