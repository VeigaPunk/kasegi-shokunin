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
                            tail, sha256sum, cat, cut, tr, sort without
                            -o/--output/--compress-program (R69: nor any abbreviation of the two
                            long flags, nor a short-option bundle carrying o), git show without
                            --output/--ext-diff/--textconv (or their abbreviations) and only
                            for blob/tree operands rev:path (R69: no commit, range, `:/` search
                            or braced operand), git cat-file without --textconv/--filters, and
                            python/python3 running a counter whose decoded script argument
                            starts literally with corpus/instruments/ and resolves inside it).
                            The same decoded argv is validated and executed. Supported syntax:
                            quoting/backslash escapes, pipelines, &&, and < file input.
                            Unquoted expansion syntax and dollar/backticks in double quotes are
                            refused; single-quoted regexes stay literal. No awk or sed. NOT a sandbox:
                            counters, unscreened flags, PATH binaries, Git configuration and
                            filesystem races can still write or execute other programs.

Exit codes: 0 every figure re-derives; 1 any figure stale or derive failed
(fail-closed: nonzero or signal final status, upstream positive status other than grep exit1,
or a non-exempt upstream signal — SIGPIPE from a read-only head with more than one counted
input operand (or from an option-carrying cat) is stale —
or empty stdout is stale);
2 harness/read error (ledger missing/unparsable, entry malformed, derive refused).
After all pipeline stages finish, a nonzero final status takes precedence: a nonzero exit is
reported as derive-exit-N and a final stage killed by signal N as derive-signal-N. Otherwise
the first upstream status that is >1, or exit1 from a program other than grep, is stale
(derive-upstream-exit-N), and an upstream stage killed by signal N is stale
(derive-upstream-signal-N). Grep exit1 is an ordinary no-match and is not an error. SIGPIPE
(-13) on a non-final stage stays benign by documented rule; for a read-only head the
exemption now applies only when the decoded argv names at most one counted input operand
(R67).  For cat the round-66 rule is applied first and unchanged: no operands (stdin) or
exactly one operand with no options (a lone "-" operand counts as a stdin input; a leading
"--" separator is honored; ANY option token is refused conservatively).  For the other
read-only heads the count is conservative: the decoded argv is split at the FIRST "--"
separator anywhere in it (a leading "--" is the same first split), grep's pattern is skipped
as a required non-file argument among the pre-separator tokens, a pre-separator token
starting with "-" that is not "-" itself is an option and not an operand, everything
pre-separator that is not an option counts, and EVERYTHING after the separator counts —
end of options makes dash-named files real operands — so pre-separator option VALUES
inflate the count and cause a safe stale.  Unknown heads retain the benign rule.  A
read-only head with two or more counted inputs goes stale derive-upstream-signal-N: with
multiple inputs the truncation can hide a later operand's error (observed false greens at
base: large `cat big.txt missing.txt | head -n 1` (R66) and, with the same masking,
`cut -f1 -d: big.txt missing.txt | head -n 1`, `wc -l big.txt missing.txt | head -n 1`,
`grep x xlines.txt missing.txt | head -n 1` (R67)).  This is not general error detection
or pipefail. && stops a derive at the first stale group and
concatenates successful group stdout; it is not bash pipeline-status equivalence.
--selftest builds fixtures under $HYAKU_SCRATCH, otherwise $TMPDIR/the system temp
directory, and uses the current Python interpreter. It exits 0 only if all cases pass.
"""

import json
import os
import shutil
import shlex
import signal
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
    ("sort", ("-o", "--output", "--compress-program")),
    ("git show", ("--output", "--ext-diff", "--textconv")),
    ("git cat-file", ("--textconv", "--filters")),
)
# R68: the two flags above were admitted at base and really executed a program
# (`sort --compress-program=PROG` ran PROG 18288 times on one 480000-byte fixture; `git show
# --textconv` ran the config-declared driver once).  They are program-execution classes, not
# read-only derives, so they are refused at parse time like the round-60 write flags.
# R69: the round-68 wave showed the refusal was spelling-exact, not class-level
# (`.ufo/waves/round-68/w1/{CriticC1,RevengerC1}.md`).  Three rules close the measured shapes:
#   * a long option is refused when its name (text before "=") is a prefix of a denied long flag,
#     because getopt_long accepts unique abbreviations (`--compress-prog=`, `--co`, `--outp=`);
#   * for sort, a short-option bundle containing "o" (`-uo FILE`, `-ro FILE`) is refused;
#   * `git cat-file --textconv/--filters` are refused, and `git show` is admitted only for
#     blob/tree operands (`git_show_operands_ok`): a commit operand renders a patch through the
#     attribute-declared textconv driver with no flag at all.


EXPECTED_CASES = 86  # R17 pin: a dropped selftest case turns the selftest red (R65: 59 + 4; R66: +4 cat SIGPIPE shape; R67: +4 multi-head SIGPIPE input count; +2 end-of-options dash-file; R68: +4 program-execution flag refusal; R69: +9 class refusal)


def eprint(*a):
    print(*a, file=sys.stderr)


def cat_sigpipe_exempt(argv):
    """True when a SIGPIPE'd cat head had at most one decoded input: no operands (stdin) or
    exactly one operand.  A leading "--" separator is honored; a lone "-" operand counts as a
    stdin input; one filename containing spaces or quoted operators is already one decoded
    argv token.  ANY option token (a word starting with "-" that is not "-" itself, unless it
    follows a leading "--") is refused conservatively: option value semantics are not parsed
    here, so e.g. `cat -n big.txt` is stale even though it reads a single file.  This is a
    capability restriction, not general argument validation.
    """
    tokens = list(argv[1:])
    if tokens and tokens[0] == "--":
        tokens = tokens[1:]
    elif any(t.startswith("-") and t != "-" for t in tokens):
        return False
    return len(tokens) <= 1


# Non-file arguments a read-only head requires before its input operands begin: grep's
# pattern is not an input; every other read-only head takes its operands directly.
SIGPIPE_REQUIRED_NONFILE_ARGS = {"grep": 1}


def sigpipe_input_count(head, argv):
    """Conservatively count the input operands named by a SIGPIPE'd read-only stage's argv.

    The decoded argv is split at the FIRST "--" anywhere in argv[1:]: tokens before it are
    options when they start with "-" (a lone "-" counts as a stdin input) and the head's
    required non-file arguments (for grep, the pattern) are skipped among them; tokens
    after the "--" are ALL operands regardless of a leading "-", because end-of-options
    makes dash-named files real operands (critic shapes S3/S4: `cut -f1 -d: big.txt --
    -missing.txt` SIGPIPEs with "-missing.txt" never opened while the count without the
    split sees one input).  A leading "--" is simply the first split, so round-66
    behaviour is unchanged.  Before the split, option VALUES therefore inflate the count —
    which can only cause a safe stale, never a false exemption.  This is a capability
    count, not general argument validation.
    """
    tokens = list(argv[1:])
    for i, t in enumerate(tokens):
        if t == "--":
            pre, post = tokens[:i], tokens[i + 1:]
            break
    else:
        pre, post = tokens, []
    for _ in range(SIGPIPE_REQUIRED_NONFILE_ARGS.get(head, 0)):
        if pre:
            pre = pre[1:]
    return sum(1 for t in pre if not (t.startswith("-") and t != "-")) + len(post)


def upstream_stale(head, stage_argv, status):
    """Stale upstream statuses: any >1, exit1 from a program other than grep, or a signal.

    Grep exit1 is an ordinary no-match. A negative status is a signal: stale unless it is
    SIGPIPE (-13) on a stage whose head names at most one input operand.  The round-66 cat
    rule is applied first and byte-identical: a cat is exempt only with stdin-only or
    exactly one operand, no options, optional leading -- separator.  Every other read-only
    head is exempt only when the conservative operand count (sigpipe_input_count) is at
    most one; a multi-input stage is stale because the truncation can hide a later
    operand's error (R67 repair — base exempted every non-cat head blindly).  Unknown
    heads keep the old benign rule.  stage_argv is the decoded argv of the killed stage
    (never a shell string); passing it is the R66 repair — base decided SIGPIPE on the
    status alone.
    """
    if status < 0:
        if status != -signal.SIGPIPE:
            return True
        head_name = os.path.basename(head)
        if head_name == "cat":
            return not cat_sigpipe_exempt(stage_argv)
        if head_name in READ_ONLY_HEADS:
            return sigpipe_input_count(head_name, stage_argv) > 1
        return False
    if status > 1:
        return True
    return status == 1 and os.path.basename(head) != "grep"


def run_derive(plan, root):
    """Execute the already validated argv plan, never a shell string."""
    output = []
    deadline = time.monotonic() + 300
    for pipeline in plan:
        processes, files, heads, stage_argvs = [], [], [], []
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
                stage_argvs.append(list(argv))
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
                if status < 0:
                    return None, out, "derive-signal-%d" % -status
                return None, out, "derive-exit-%d" % status
            for p, head, stage_argv in zip(processes[:-1], heads[:-1], stage_argvs[:-1]):
                if upstream_stale(head, stage_argv, p.returncode):
                    out = b"".join(output).decode("utf-8", "replace").strip()
                    if p.returncode < 0:
                        return None, out, "derive-upstream-signal-%d" % -p.returncode
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
    """Check decoded option tokens, including quoted/escaped and abbreviated flag spellings."""
    for name, flags in DENIED_FLAGS:
        prefix = name.split()
        if parts[:len(prefix)] == prefix:
            for tok in parts[len(prefix):]:
                long_name = tok.split("=", 1)[0] if tok.startswith("--") else None
                for flag in flags:
                    if tok == flag or tok.startswith(flag + "="):
                        return True
                    # R69: getopt_long admits any unique abbreviation of a long option.
                    if long_name and len(long_name) > 2 and flag.startswith("--") \
                            and flag.startswith(long_name):
                        return True
                    # R69: a short-option bundle carrying "o" (`-uo FILE`) is sort's -o.
                    if flag == "-o" and tok.startswith("-") and not tok.startswith("--") \
                            and "o" in tok[1:]:
                        return True
    return False


def git_show_operands_ok(parts):
    """R69: admit `git show` only for blob/tree operands (`rev:path`, `rev:`, `:path`).

    A commit, tag or range operand (or no operand, which means HEAD) renders a patch, and the
    patch runs an attribute-declared textconv driver with no flag.  `:/text` searches commit
    messages and resolves to a commit; a colon inside `{...}` (`rev^{/a:b}`) is not the path
    separator, so any brace is refused; `--` would turn later tokens into pathspecs.
    """
    operands = [t for t in parts[2:] if not t.startswith("-")]
    if "--" in parts[2:] or not operands:
        return False
    for t in operands:
        if ":" not in t or t.startswith(":/") or "{" in t or "}" in t:
            return False
    return True


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
        if len(parts) > 1 and parts[1] == "show":
            return git_show_operands_ok(parts)
        return len(parts) > 1 and parts[1] in ("cat-file", "ls-tree")
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

    def run_case(cid, want_exit, ledger_doc=None, broken=False, reason=None, big=False):
        tmp = tempfile.mkdtemp(prefix="figure-audit-selftest-",
                               dir=os.environ.get("HYAKU_SCRATCH") or None)
        try:
            with open(os.path.join(tmp, "g.txt"), "w", encoding="utf-8", newline="\n") as f:
                f.write("35\n")
            with open(os.path.join(tmp, "f1.txt"), "w", encoding="utf-8", newline="\n") as f:
                f.write("340\n")
            if big:
                # R66: 4 MiB deterministic fixtures starting "alpha"/"beta".  A first operand
                # this size far exceeds the 64 KiB pipe buffer, so `cat big.txt ... | head -n 1`
                # delivers SIGPIPE to cat (base red receipt native_statuses=141) before cat can
                # finish; small fixtures do not SIGPIPE and stay on the exit-status paths.
                with open(os.path.join(tmp, "big.txt"), "w", encoding="utf-8", newline="\n") as f:
                    f.write("alpha\n" + ("x" * 1023 + "\n") * 4095)
                with open(os.path.join(tmp, "other.txt"), "w", encoding="utf-8", newline="\n") as f:
                    f.write("beta\n" + ("y" * 1023 + "\n") * 4095)
                with open(os.path.join(tmp, "xlines.txt"), "w", encoding="utf-8", newline="\n") as f:
                    f.write("x\n" * 200000)
            os.makedirs(os.path.join(tmp, "corpus", "instruments"), exist_ok=True)
            with open(os.path.join(tmp, "corpus", "instruments", "ok.py"), "w", encoding="utf-8", newline="\n") as f:
                f.write("print(35)\n")
            with open(os.path.join(tmp, "corpus", "instruments", "fail.py"), "w", encoding="utf-8", newline="\n") as f:
                f.write("raise SystemExit(7)\n")
            with open(os.path.join(tmp, "corpus", "instruments", "exit1.py"), "w", encoding="utf-8", newline="\n") as f:
                f.write("raise SystemExit(1)\n")
            with open(os.path.join(tmp, "corpus", "instruments", "kill.py"), "w", encoding="utf-8", newline="\n") as f:
                f.write("import os, signal\nos.kill(os.getpid(), signal.SIGTERM)\n")
            with open(os.path.join(tmp, "corpus", "instruments", "kill9.py"), "w", encoding="utf-8", newline="\n") as f:
                f.write("import os, signal, sys\nsys.stdout.write('35\\n')\nsys.stdout.flush()\nos.kill(os.getpid(), signal.SIGKILL)\n")
            with open(os.path.join(tmp, "corpus", "instruments", "pipe.py"), "w", encoding="utf-8", newline="\n") as f:
                f.write("import signal, sys\nsignal.signal(signal.SIGPIPE, signal.SIG_DFL)\nsys.stdout.write(('x' * 1023 + '\\n') * 4096)\nsys.stdout.flush()\n")
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
            # The end-of-options cases name "-missing.txt" as a dash-named operand; the
            # fixture must NOT create it, and the absence is asserted, not assumed.
            assert not os.path.exists(os.path.join(tmp, "-missing.txt"))
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
            reasons = reason if isinstance(reason, tuple) else ((reason,) if reason else ())
            good = p.returncode == want_exit and (not reasons or any("reason=%s stale" % r in out for r in reasons))
            observed = ",".join(dict.fromkeys(
                ln.split("reason=", 1)[1].split(" stale", 1)[0]
                for ln in out.splitlines() if "reason=" in ln and " stale" in ln))
            cases.append((cid, p.returncode, want_exit, good, out, observed))
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
    run_case("git-show-output-flag-refused", 2, _one("s-gito", "git show --output=out.txt HEAD:g.txt", "35"))
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
    run_case("git-quoted-output-refused", 2, _one("s-gitquote", "git show '--output=out.txt' HEAD:g.txt", "35"))
    run_case("sort-compress-program-refused", 2,
             _one("s-sortcompress", "sort --compress-program=/bin/false -S 1K g.txt | head -n 1", "35"))
    run_case("sort-compress-program-space-refused", 2,
             _one("s-sortcompress2", "sort --compress-program /bin/false g.txt", "35"))
    run_case("sort-compress-program-quoted-refused", 2,
             _one("s-sortcompress3", "sort '--compress-program=/bin/false' g.txt", "35"))
    run_case("git-show-textconv-refused", 2,
             _one("s-gittextconv", "git show --textconv HEAD:g.txt", "35"))
    # R69: class-level refusals.  Each derive isolates one rule: the flag cases name a blob
    # operand (so only the flag rule refuses them) and the git-show operand cases carry no flag.
    run_case("sort-compress-prefix-refused", 2,
             _one("s-sortprefix", "sort --compress-prog=/bin/false -S 1K g.txt | head -n 1", "35"))
    run_case("sort-compress-short-prefix-space-refused", 2,
             _one("s-sortprefix2", "sort --co /bin/false g.txt", "35"))
    run_case("sort-output-prefix-refused", 2, _one("s-sortoutp", "sort --outp=out.txt g.txt", "35"))
    run_case("sort-bundled-short-o-refused", 2, _one("s-sortuo", "sort -uo out.txt g.txt", "35"))
    run_case("git-show-commit-form-refused", 2, _one("s-gitcommit", "git show HEAD", "35"))
    run_case("git-show-message-search-refused", 2, _one("s-gitsearch", "git show ':/fixture'", "35"))
    run_case("git-show-brace-colon-refused", 2, _one("s-gitbrace", "git show 'HEAD^{/a:b}'", "35"))
    run_case("git-cat-file-textconv-refused", 2,
             _one("s-catfiletc", "git cat-file --textconv HEAD:g.txt", "35"))
    run_case("git-cat-file-filters-refused", 2,
             _one("s-catfilefi", "git cat-file --filters HEAD:g.txt", "35"))
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
    # R65: flipped from exit 0. A signal-killed producer is stale (fail-closed); id kept for lineage.
    run_case("upstream-python-signal-ignored", 1, _one("s-pysignal", "python3 corpus/instruments/kill.py | wc -l", "0"),
             reason="derive-upstream-signal-15")
    run_case("upstream-grep-count-nomatch-ignored", 0, _one("s-grepcount", "grep -c absent g.txt | wc -l", "1"))
    run_case("upstream-middle-sigterm-stale", 1, _one("s-midsig", "cat g.txt | python3 corpus/instruments/kill.py | wc -l", "0"),
             reason="derive-upstream-signal-15")
    run_case("upstream-python-sigkill-stale", 1, _one("s-sigkill", "python3 corpus/instruments/kill9.py | wc -l", "1"),
             reason="derive-upstream-signal-9")
    run_case("final-stage-signal-stale", 1, _one("s-finalsig", "python3 corpus/instruments/kill.py", "0"),
             reason="derive-signal-15")
    run_case("upstream-sigpipe-nonfinal-benign", 0, _one("s-sigpipe", "python3 corpus/instruments/pipe.py | head -n 1 | wc -l", "1"))
    # R66 cat-shape restriction: the SIGPIPE exemption needs stdin-only or exactly one
    # decoded operand.  Cases 1-2 are the base false green (base red receipt: exit 0 with
    # native cat status -13) — the candidate must refuse them.  The audit reason is asserted,
    # never an assumed native status; a timing fluke downgrading cat to exit 1 would surface
    # as derive-upstream-exit-1 and fail these cases loudly rather than pass silently.
    run_case("upstream-cat-multi-missing-sigpipe-stale", 1,
             _one("s-catmulti", "cat big.txt missing.txt | head -n 1", "alpha"),
             reason="derive-upstream-signal-13", big=True)
    run_case("upstream-cat-multi-existing-sigpipe-stale", 1,
             _one("s-catmulti2", "cat big.txt other.txt | head -n 1", "alpha"),
             reason="derive-upstream-signal-13", big=True)
    # Cases 3-4: a single decoded input stays benign (green at base too).
    run_case("upstream-cat-single-operand-sigpipe-benign", 0,
             _one("s-catone", "cat big.txt | head -n 1", "alpha"), big=True)
    run_case("upstream-cat-stdin-sigpipe-benign", 0,
             _one("s-catstdin", "cat < big.txt | head -n 1", "alpha"), big=True)
    # R67 multi-head input-count rule: the SIGPIPE exemption now needs at most one counted
    # input operand for every read-only head (grep's pattern is a required non-file
    # argument, not an input).  Cases 1-3 are the C1 control probes P9/P10/P11; their
    # native stage-0 status has FACE variance on this host (controls/face-matrix-r67.txt:
    # pi-uu-grep 0.2.0 gives -13 when SIGPIPE wins the race and 2 when it reaches the
    # missing operand first; cut shows a 1 face), so they assert the VERDICT — stale —
    # under any of the three refusal reasons, never one frozen reason.  The -13 face is
    # the one the new rule refuses; the exit faces were already refused by the status
    # rule.  The observed reason(s) are printed on each case line so the exercised face
    # is visible in the receipt.  Case 4 proves grep's pattern is not an input: a
    # single-file grep SIGPIPE stays benign; single-input positives keep exact green.
    run_case("upstream-cut-multi-missing-stale", 1,
             _one("s-cutmulti", "cut -f1 -d: big.txt missing.txt | head -n 1", "alpha"),
             reason=("derive-upstream-signal-13", "derive-upstream-exit-1", "derive-upstream-exit-2"), big=True)
    run_case("upstream-wc-multi-missing-stale", 1,
             _one("s-wcmulti", "wc -l big.txt missing.txt | head -n 1", "4096 big.txt"),
             reason=("derive-upstream-signal-13", "derive-upstream-exit-1", "derive-upstream-exit-2"), big=True)
    run_case("upstream-grep-multi-missing-stale", 1,
             _one("s-grepmulti", "grep x xlines.txt missing.txt | head -n 1", "x"),
             reason=("derive-upstream-signal-13", "derive-upstream-exit-1", "derive-upstream-exit-2"), big=True)
    run_case("upstream-grep-single-pattern-file-sigpipe-benign", 0,
             _one("s-grepone", "grep x big.txt | head -n 1", "x" * 1023), big=True)
    # R67 end-of-options hole (critic shapes S3/S4): a NON-leading "--" ends the options,
    # so every token after it is a real operand and "-missing.txt" is a dash-named file the
    # count must see.  The differential `cut -f1 -d: big.txt -missing.txt` exits 1 (cut
    # treats the bare token as an unknown option), proving the "--" form is what names the
    # operand.  Native stage0 was -13 with "-missing.txt" never opened and the gate read ok
    # before the split fix; the cases assert the stale verdict under any of the three
    # refusal reasons, and the fixture creates no "-missing.txt" (absence asserted above).
    run_case("upstream-cut-dashfile-after-separator-stale", 1,
             _one("s-cutdash", "cut -f1 -d: big.txt -- -missing.txt | head -n 1", "alpha"),
             reason=("derive-upstream-signal-13", "derive-upstream-exit-1", "derive-upstream-exit-2"), big=True)
    run_case("upstream-grep-dashfile-after-separator-stale", 1,
             _one("s-grepdash", "grep x xlines.txt -- -missing.txt | head -n 1", "x"),
             reason=("derive-upstream-signal-13", "derive-upstream-exit-1", "derive-upstream-exit-2"), big=True)
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
    run_case("upstream-git-missing-ref-stale", 1, _one("s-gitmissing", "git show refs/figure-audit-nonexistent:g.txt | wc -l", "0"),
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
    for cid, got, want, good, out, observed in cases:
        print("selftest case=%s exit=%d want=%d verdict=%s%s" % (
            cid, got, want, "pass" if good else "fail", (" reasons=" + observed) if observed else ""))
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
