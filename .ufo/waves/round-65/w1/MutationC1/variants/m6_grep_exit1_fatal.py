#!/usr/bin/env python
"""figure-audit.py — re-derive figures recorded in lane records against committed bytes.

The r53 closure routed two number-drift defects (D53-1: a receipt trailer said
"34 inherited" while the same receipt's measured line printed
FAIL_entry_records=33; D53-2: capture metadata said 543 lines while `wc -l`
over the committed capture printed 542).  This instrument is the audit that
catches that class: a JSON ledger pins, per figure, where it is recorded, the
literal as recorded, a read-only command that re-derives it, and the value the
command must print.  Every figure is re-derived and compared as a WHOLE value
(never a substring), so a recorded 34 against a derived 33, or a want of 34
against a derived 340, reads stale.

Usage:
  python corpus/instruments/figure-audit.py [--ledger PATH] [--root DIR]

Ledger entry shape (JSON object with a "figures" array):
  {"id": "...",      - stable figure id
   "record": "...",  - where the literal is recorded (file:line or pointer)
   "recorded": "...",- the literal as recorded (informational, printed)
   "derive": "...",  - literal-argv command grammar, run with cwd=root (no shell)
   "want": "...",    - the exact value the command must print (stripped)
   optional "rev": "..."} - when present, "derive" should address committed
                            bytes at that rev (e.g. `git show <rev>:<path>`);
                            entries require an allow-listed head
                            (allow-list: git show, git cat-file, git ls-tree, grep, wc, ls, head,
                            tail, sha256sum, cat, cut, tr, sort without -o/--output, and
                            python/python3 running a counter whose decoded script argument
                            starts literally with corpus/instruments/ and resolves inside it).
                            The same decoded argv is validated and executed. Supported syntax:
                            quoting/backslash escapes, pipelines, &&, and < file input.
                            Unquoted expansion syntax and dollar/backticks in double quotes are
                            refused; single-quoted regexes stay literal. No awk or sed. NOT a sandbox:
                            counters, unscreened flags, PATH binaries, Git configuration and
                            filesystem races can still write or execute other programs.

Exit codes: 0 every figure re-derives; 1 any figure stale or derive failed
(fail-closed: nonzero final status, upstream positive status other than grep exit1,
or empty stdout is stale);
2 harness/read error (ledger missing/unparsable, entry malformed, derive refused).
After all pipeline stages finish, a nonzero final status takes precedence
(derive-exit-N); otherwise the first upstream status that is >1, or exit1 from a
program other than grep, is stale (derive-upstream-exit-N). Grep exit1 is an ordinary
no-match and is not an error; negative signal statuses remain ignored. This is not
general error detection or pipefail. && stops a derive at the first stale group and
concatenates successful group stdout; it is not bash pipeline-status equivalence.
--selftest builds fixtures under $HYAKU_SCRATCH, otherwise $TMPDIR/the system temp
directory, and uses the current Python interpreter. It exits 0 only if all cases pass.
"""

import json
import os
import shutil
import shlex
import subprocess
import sys
import tempfile
import time

READ_ONLY_HEADS = (
    "grep", "wc", "ls", "sha256sum", "cat", "cut", "sort", "tr", "head", "tail",
)

# Heads whose flags can write a file or execute a configured command: refused when such a flag
# appears as a token.  A write through an allow-listed head is a write class like any other.
DENIED_FLAGS = (
    ("sort", ("-o", "--output")),
    ("git show", ("--output", "--ext-diff")),
)


EXPECTED_CASES = 59  # R17 pin: a dropped selftest case turns the selftest red


def eprint(*a):
    print(*a, file=sys.stderr)


def upstream_stale(head, status):
    """Stale upstream statuses: any >1, or exit1 from a program other than grep.

    Grep exit1 is an ordinary no-match; negative (signal) statuses stay ignored.
    """
    if status > 1:
        return True
    return status == 1  # mutant: grep exit1 no longer exempt


def run_derive(plan, root):
    """Execute the already validated argv plan, never a shell string."""
    output = []
    deadline = time.monotonic() + 300
    for pipeline in plan:
        processes, files, heads = [], [], []
        previous = None
        try:
            for argv, input_path in pipeline:
                stdin = previous
                if input_path is not None:
                    stdin = open(os.path.join(root or ".", input_path), "rb")
                    files.append(stdin)
                errors = tempfile.TemporaryFile()
                files.append(errors)
                p = subprocess.Popen(argv, cwd=root or ".", stdin=stdin,
                                     stdout=subprocess.PIPE, stderr=errors)
                processes.append(p)
                heads.append(argv[0])
                if previous is not None:
                    previous.close()
                previous = p.stdout
            raw, _ = processes[-1].communicate(timeout=max(0, deadline - time.monotonic()))
            for p in processes[:-1]:
                p.wait(timeout=max(0, deadline - time.monotonic()))
            output.append(raw)
            status = processes[-1].returncode
            if status != 0:
                out = b"".join(output).decode("utf-8", "replace").strip()
                return None, out, "derive-exit-%d" % status
            for p, head in zip(processes[:-1], heads[:-1]):
                if upstream_stale(head, p.returncode):
                    out = b"".join(output).decode("utf-8", "replace").strip()
                    return None, out, "derive-upstream-exit-%d" % p.returncode
        except subprocess.TimeoutExpired:
            return None, "", "derive-timeout"
        except (OSError, ValueError) as e:
            return None, "", "derive-exec-error-%s" % type(e).__name__
        finally:
            for p in processes:
                if p.poll() is None:
                    p.kill()
            for p in processes:
                p.wait()
                if p.stdout is not None:
                    p.stdout.close()
            for f in files:
                f.close()
    out = b"".join(output).decode("utf-8", "replace").strip()
    if not out:
        return None, out, "derive-empty"
    return out, out, None


def tokenize(cmd):
    """Tag operators before shlex decoding, so quoted separators stay arguments."""
    if not isinstance(cmd, str) or any(c in cmd for c in "\0\n\r"):
        return None
    tokens, word, quote, i = [], [], None, 0

    def flush():
        if word:
            tokens.append(("word", shlex.split("".join(word), posix=True)[0]))
            word.clear()

    try:
        while i < len(cmd):
            c = cmd[i]
            if quote == "'":
                word.append(c)
                if c == "'":
                    quote = None
            elif quote == '"':
                if c in "$`":
                    return None
                word.append(c)
                if c == "\\" and i + 1 < len(cmd) and cmd[i + 1] in '$`"\\':
                    i += 1
                    word.append(cmd[i])
                elif c == '"':
                    quote = None
            elif c == "\\":
                if i + 1 == len(cmd):
                    return None
                word.extend((c, cmd[i + 1]))
                i += 1
            elif c in "'\"":
                quote = c
                word.append(c)
            elif c.isspace():
                flush()
            elif c in "|&<":
                flush()
                if c == "&":
                    if cmd[i:i + 2] != "&&":
                        return None
                    tokens.append(("op", "&&"))
                    i += 1
                else:
                    tokens.append(("op", c))
            elif c in ";>()$`*?[]{}~#":
                return None
            else:
                word.append(c)
            i += 1
        if quote is not None:
            return None
        flush()
    except ValueError:
        return None
    return tokens


def denied_flag(parts):
    """Check decoded option tokens, including quoted/escaped flag spellings."""
    for name, flags in DENIED_FLAGS:
        prefix = name.split()
        if parts[:len(prefix)] == prefix:
            for tok in parts[len(prefix):]:
                for flag in flags:
                    if tok == flag or tok.startswith(flag + "="):
                        return True
                    if flag == "-o" and tok.startswith("-o") and tok != "-o":
                        return True
    return False


def python_head_ok(root, parts):
    """Require both a literal decoded prefix and a separator-bounded realpath."""
    if len(parts) < 2 or not parts[1].replace("\\", "/").startswith("corpus/instruments/"):
        return False
    base = os.path.realpath(os.path.join(root or ".", "corpus", "instruments"))
    target = os.path.realpath(os.path.join(root or ".", parts[1]))
    if target == base:
        return False
    return target.startswith(base + os.sep)


def segment_ok(root, parts):
    if parts[0] in ("python", "python3"):
        return python_head_ok(root, parts)
    if denied_flag(parts):
        return False
    if parts[0] == "git":
        return len(parts) > 1 and parts[1] in ("show", "cat-file", "ls-tree")
    return parts[0] in READ_ONLY_HEADS


def parse_derive(root, cmd):
    """Parse and validate once; the resulting argv objects are executed unchanged."""
    tokens = tokenize(cmd)
    if not tokens:
        return None
    plan, pipeline, argv, input_path = [], [], [], None
    i = 0
    while i < len(tokens):
        kind, value = tokens[i]
        if kind == "word":
            argv.append(value)
        elif value == "<":
            # Input redirection is deliberately limited to the first pipeline stage.
            if input_path is not None or pipeline or i + 1 == len(tokens):
                return None
            i += 1
            if tokens[i][0] != "word":
                return None
            input_path = tokens[i][1]
        else:
            if not argv or not segment_ok(root, argv):
                return None
            pipeline.append((argv, input_path))
            argv, input_path = [], None
            if value == "&&":
                plan.append(pipeline)
                pipeline = []
        i += 1
    if not argv or not segment_ok(root, argv):
        return None
    pipeline.append((argv, input_path))
    plan.append(pipeline)
    return plan


def check_read_only(root, cmd):
    return parse_derive(root, cmd) is not None


def audit(ledger_path, root):
    try:
        with open(ledger_path, "r", encoding="utf-8") as f:
            doc = json.load(f)
    except FileNotFoundError:
        eprint("FIGURE-AUDIT: UNAVAILABLE reason=ledger-missing path=%s" % ledger_path)
        return 2
    except (ValueError, UnicodeDecodeError) as e:
        eprint("FIGURE-AUDIT: UNAVAILABLE reason=ledger-unreadable detail=%s" % e)
        return 2
    figs = doc.get("figures") if isinstance(doc, dict) else None
    if not isinstance(figs, list) or not figs:
        eprint("FIGURE-AUDIT: UNAVAILABLE reason=ledger-shape want=figures-array")
        return 2
    ok = stale = 0
    for ent in figs:
        if not isinstance(ent, dict) or not all(k in ent for k in ("id", "record", "recorded", "derive", "want")):
            eprint("FIGURE-AUDIT: UNAVAILABLE reason=entry-shape entry=%r" % (ent.get("id") if isinstance(ent, dict) else ent,))
            return 2
        plan = parse_derive(root, ent["derive"])
        if plan is None:
            eprint("FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=%s" % ent["id"])
            return 2
        derived, raw, err = run_derive(plan, root)
        if err is not None:
            stale += 1
            print("FIG %s recorded=%s derived=UNAVAILABLE reason=%s stale" % (ent["id"], ent["recorded"], err))
            continue
        if derived == str(ent["want"]):
            ok += 1
            print("FIG %s recorded=%s derived=%s ok" % (ent["id"], ent["recorded"], derived))
        else:
            stale += 1
            print("FIG %s recorded=%s derived=%s want=%s stale" % (ent["id"], ent["recorded"], derived, ent["want"]))
    code = 1 if stale else 0
    print("FIGURE-AUDIT figures=%d ok=%d stale=%d exit=%d" % (len(figs), ok, stale, code))
    return code


SELFTEST_LEDGER_OK = {
    "figures": [
        {"id": "s-ok", "record": "g.txt:1", "recorded": "35", "derive": "cat g.txt", "want": "35"},
    ],
}
SELFTEST_LEDGER_STALE = {
    "figures": [
        {"id": "s-stale", "record": "f1.txt:1", "recorded": "7", "derive": "cat f1.txt", "want": "7"},
    ],
}
SELFTEST_LEDGER_FAILS = {
    "figures": [
        {"id": "s-fails", "record": "missing.txt", "recorded": "1", "derive": "cat missing.txt", "want": "1"},
    ],
}
SELFTEST_LEDGER_TOKEN = {
    "figures": [
        {"id": "s-token", "record": "f1.txt:1", "recorded": "34", "derive": "cat f1.txt", "want": "34"},
    ],
}


SELFTEST_LEDGER_NOT_RO = {
    "figures": [
        {"id": "s-not-ro", "record": "g.txt:1", "recorded": "35", "derive": "echo 35", "want": "35"},
    ],
}

def _one(fid, derive, want):
    return {"figures": [{"id": fid, "record": "g.txt:1", "recorded": want, "derive": derive, "want": want}]}


def selftest():
    cases = []

    def run_case(cid, want_exit, ledger_doc=None, broken=False, reason=None):
        tmp = tempfile.mkdtemp(prefix="figure-audit-selftest-",
                               dir=os.environ.get("HYAKU_SCRATCH") or None)
        try:
            with open(os.path.join(tmp, "g.txt"), "w", encoding="utf-8", newline="\n") as f:
                f.write("35\n")
            with open(os.path.join(tmp, "f1.txt"), "w", encoding="utf-8", newline="\n") as f:
                f.write("340\n")
            os.makedirs(os.path.join(tmp, "corpus", "instruments"), exist_ok=True)
            with open(os.path.join(tmp, "corpus", "instruments", "ok.py"), "w", encoding="utf-8", newline="\n") as f:
                f.write("print(35)\n")
            with open(os.path.join(tmp, "corpus", "instruments", "fail.py"), "w", encoding="utf-8", newline="\n") as f:
                f.write("raise SystemExit(7)\n")
            with open(os.path.join(tmp, "corpus", "instruments", "exit1.py"), "w", encoding="utf-8", newline="\n") as f:
                f.write("raise SystemExit(1)\n")
            with open(os.path.join(tmp, "corpus", "instruments", "kill.py"), "w", encoding="utf-8", newline="\n") as f:
                f.write("import os, signal\nos.kill(os.getpid(), signal.SIGTERM)\n")
            with open(os.path.join(tmp, "corpus", "instruments", "grep.py"), "w", encoding="utf-8", newline="\n") as f:
                f.write("raise SystemExit(1)\n")
            with open(os.path.join(tmp, "out.py"), "w", encoding="utf-8", newline="\n") as f:
                f.write("print(35)\n")
            os.makedirs(os.path.join(tmp, "corpus", "instruments2"))
            with open(os.path.join(tmp, "corpus", "instruments2", "ok.py"),
                      "w", encoding="utf-8", newline="\n") as f:
                f.write("print(35)\n")
            try:
                os.symlink(os.path.join(tmp, "out.py"),
                           os.path.join(tmp, "corpus", "instruments", "link.py"))
            except (OSError, NotImplementedError):
                pass
            lp = os.path.join(tmp, "ledger.json")
            with open(lp, "w", encoding="utf-8", newline="\n") as f:
                if broken:
                    f.write("{not json")
                else:
                    json.dump(ledger_doc, f)
                    f.write("\n")
            me = os.path.abspath(sys.argv[0])
            p = subprocess.run([sys.executable, me, "--ledger", lp, "--root", tmp],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
            out = p.stdout.decode("utf-8", "replace")
            good = p.returncode == want_exit and (reason is None or "reason=%s stale" % reason in out)
            cases.append((cid, p.returncode, want_exit, good, out))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    run_case("ok-ledger", 0, SELFTEST_LEDGER_OK)
    run_case("stale-literal", 1, SELFTEST_LEDGER_STALE)
    run_case("derive-fails-fail-closed", 1, SELFTEST_LEDGER_FAILS)
    run_case("token-boundary-34-vs-340", 1, SELFTEST_LEDGER_TOKEN)
    run_case("unreadable-ledger-exit-2", 2, None, broken=True)
    run_case("derive-not-read-only-refused", 2, SELFTEST_LEDGER_NOT_RO)
    run_case("chain-semicolon-refused", 2, _one("s-semi", "cat g.txt; cat g.txt", "35"))
    run_case("chain-background-refused", 2, _one("s-bg", "cat g.txt & true", "35"))
    run_case("chain-newline-refused", 2, _one("s-nl", "cat g.txt\ncat g.txt", "35"))
    run_case("chain-cmdsubst-refused", 2, _one("s-subst", "cat g.txt $(cat g.txt)", "35"))
    run_case("pipe-to-shell-refused", 2, _one("s-sh", "cat g.txt | sh", "35"))
    run_case("redirect-refused", 2, _one("s-redir", "cat g.txt > out.txt", "35"))
    run_case("or-chain-refused", 2, _one("s-or", "cat nosuch.txt || cat g.txt", "35"))
    run_case("quoted-separator-admitted", 0, _one("s-quoted", "cat g.txt | grep -e '35' -e ';'", "35"))
    run_case("escape-single-quote-refused", 2, _one("s-esc1", "cat g.txt \\'; touch X; \\'", "35"))
    run_case("escape-double-quote-refused", 2, _one("s-esc2", "cat g.txt \\\"; touch X; \\\"", "35"))
    run_case("sed-head-refused", 2, _one("s-sed", "sed -n '1e touch X' g.txt", "35"))
    run_case("awk-head-refused", 2, _one("s-awk", "awk 'BEGIN{system(\"touch X\")}'", "35"))
    run_case("sort-output-flag-refused", 2, _one("s-sorto", "sort -o out.txt g.txt", "35"))
    run_case("git-show-output-flag-refused", 2, _one("s-gito", "git show --output=out.txt HEAD", "35"))
    run_case("python-inside-admitted", 0, _one("s-pyin", "python3 corpus/instruments/ok.py", "35"))
    run_case("python-traversal-refused", 2, _one("s-pytrav", "python3 corpus/instruments/../../out.py", "35"))
    run_case("python-symlink-refused", 2, _one("s-pylink", "python3 corpus/instruments/link.py", "35"))
    run_case("python-absolute-refused", 2, _one("s-pyabs", "python3 /nonexistent-absolute.py", "35"))
    run_case("python-quoted-traversal-refused", 2, _one("s-pyquote", 'python3 corpus/instruments/"../../out.py"', "35"))
    run_case("python-dot-prefix-refused", 2, _one("s-pydot", "python3 ./corpus/instruments/ok.py", "35"))
    run_case("python-sibling-boundary-refused", 2, _one("s-pysibling", "python3 corpus/instruments/../instruments2/ok.py", "35"))
    run_case("dollar-expansion-refused", 2, _one("s-dollar", "cat $HOME/g.txt", "35"))
    run_case("double-quoted-expansion-refused", 2, _one("s-dq", 'cat "${HOME}/g.txt"', "35"))
    run_case("sort-quoted-output-refused", 2, _one("s-sortquote", "sort '-o' out.txt g.txt", "35"))
    run_case("sort-escaped-output-refused", 2, _one("s-sortescape", r"sort -\o out.txt g.txt", "35"))
    run_case("git-quoted-output-refused", 2, _one("s-gitquote", "git show '--output=out.txt' HEAD", "35"))
    run_case("input-redirection-admitted", 0, _one("s-input", "cat < g.txt", "35"))
    run_case("and-shortcircuit-fails", 1, _one("s-andfail", "cat missing.txt && cat g.txt", "35"))
    run_case("and-stdout-concatenated", 0, _one("s-andout", "cat g.txt && cat g.txt", "35\n35"))
    run_case("upstream-cat-missing-exit1-stale", 1, _one("s-catmissing", "cat missing.txt | wc -l", "0"),
             reason="derive-upstream-exit-1")
    run_case("upstream-cat-partial-exit1-stale", 1, _one("s-catpartial", "cat g.txt missing.txt | wc -l", "1"),
             reason="derive-upstream-exit-1")
    run_case("upstream-cut-missing-exit1-stale", 1, _one("s-cutmissing", "cut -c1 missing.txt | wc -l", "0"),
             reason="derive-upstream-exit-1")
    run_case("upstream-head-missing-exit1-stale", 1, _one("s-headmissing", "head -n 1 missing.txt | wc -l", "0"),
             reason="derive-upstream-exit-1")
    run_case("upstream-tail-missing-exit1-stale", 1, _one("s-tailmissing", "tail -n 1 missing.txt | wc -l", "0"),
             reason="derive-upstream-exit-1")
    run_case("upstream-ls-missing-exit2-stale", 1, _one("s-lsmissing", "ls missing.txt | wc -l", "0"),
             reason="derive-upstream-exit-2")
    run_case("upstream-sort-missing-exit2-stale", 1, _one("s-sortmissing", "sort missing.txt | wc -l", "0"),
             reason="derive-upstream-exit-2")
    run_case("upstream-sha256sum-missing-exit1-stale", 1, _one("s-shamissing", "sha256sum missing.txt | wc -l", "0"),
             reason="derive-upstream-exit-1")
    run_case("upstream-python-exit1-stale", 1, _one("s-pyexit1", "python3 corpus/instruments/exit1.py | wc -l", "0"),
             reason="derive-upstream-exit-1")
    run_case("upstream-python-signal-ignored", 0, _one("s-pysignal", "python3 corpus/instruments/kill.py | wc -l", "0"))
    run_case("upstream-grep-count-nomatch-ignored", 0, _one("s-grepcount", "grep -c absent g.txt | wc -l", "1"))
    run_case("final-exit7-precedes-upstream-exit1", 1, _one("s-catfinal", "cat missing.txt | python3 corpus/instruments/fail.py", "0"),
             reason="derive-exit-7")
    run_case("and-first-group-upstream-exit1-stale", 1, _one("s-andfirst", "cat missing.txt | wc -l && cat g.txt", "0"),
             reason="derive-upstream-exit-1")
    run_case("and-second-group-upstream-exit1-stale", 1, _one("s-andsecond", "cat g.txt | wc -l && cat missing.txt | wc -l", "1"),
             reason="derive-upstream-exit-1")
    run_case("middle-stage-upstream-exit1-stale", 1, _one("s-middle", "cat g.txt | cat missing.txt | wc -l", "0"),
             reason="derive-upstream-exit-1")
    run_case("named-grep-txt-cat-exit1-stale", 1, _one("s-grepname", "cat grep.txt | wc -l", "0"),
             reason="derive-upstream-exit-1")
    run_case("named-grep-py-exit1-stale", 1, _one("s-grepscript", "python3 corpus/instruments/grep.py | wc -l", "0"),
             reason="derive-upstream-exit-1")
    run_case("upstream-grep-invalid-stale", 1, _one("s-grepinvalid", "grep '[' g.txt | wc -l", "0"),
             reason="derive-upstream-exit-2")
    run_case("upstream-git-missing-ref-stale", 1, _one("s-gitmissing", "git show refs/figure-audit-nonexistent | wc -l", "0"),
             reason="derive-upstream-exit-128")
    run_case("upstream-python-exit7-stale", 1, _one("s-pyfail", "python3 corpus/instruments/fail.py | wc -l", "0"),
             reason="derive-upstream-exit-7")
    run_case("upstream-grep-no-match-counts-zero", 0, _one("s-grepzero", "grep absent g.txt | wc -l", "0"))
    run_case("successful-pipeline-counts-one", 0, _one("s-pipeok", "cat g.txt | wc -l", "1"))
    run_case("final-exit1-stale", 1, _one("s-finalone", "cat g.txt | grep absent", "0"),
             reason="derive-exit-1")
    run_case("final-error-precedes-upstream-error", 1, _one("s-finalfirst", "grep '[' g.txt | python3 corpus/instruments/fail.py", "0"),
             reason="derive-exit-7")

    failures = 0
    for cid, got, want, good, out in cases:
        print("selftest case=%s exit=%d want=%d verdict=%s" % (cid, got, want, "pass" if good else "fail"))
        if not good:
            failures += 1
    if len(cases) != EXPECTED_CASES:
        print("selftest pin cases=%d expected=%d verdict=fail" % (len(cases), EXPECTED_CASES))
        failures += 1
    print("selftest cases=%d failures=%d" % (len(cases), failures))
    return 0 if failures == 0 else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    ledger = os.path.join("corpus", "instruments", "figure-audit-ledger.json")
    root = "."
    it = iter(argv)
    for a in it:
        if a == "--ledger":
            ledger = next(it)
        elif a == "--root":
            root = next(it)
    return audit(ledger, root)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
