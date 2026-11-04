#!/usr/bin/env python3
"""Attack harness: base production run_derive vs an intended-rule candidate.

Imports the base figure-audit module unchanged (parse_derive, tokenize, segment_ok
are reused verbatim); only the upstream-status decision differs between base and
candidate.  Candidate rule (intended, from the r64 spec):
  upstream rc > 0 is stale, except basename-grep rc == 1; rc < 0 (signal) is ignored;
  final-stage nonzero still returns first (precedence) and && still short-circuits.
"""
import importlib.util
import os
import subprocess
import sys
import tempfile
import time

BASE = "/fast/scratch/hyaku/kasegi-r64/CriticPipeline/base/figure-audit.py"
WORK = "/fast/scratch/hyaku/kasegi-r64/CriticPipeline/work"

spec = importlib.util.spec_from_file_location("fa", BASE)
fa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fa)


def run_derive_rule(plan, root, rule):
    """Mirror fa.run_derive; `rule` is 'base' or 'cand' for the upstream decision."""
    output = []
    deadline = time.monotonic() + 300
    for pipeline in plan:
        processes, files = [], []
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
                processes.append((p, argv))
                if previous is not None:
                    previous.close()
                previous = p.stdout
            raw, _ = processes[-1][0].communicate(timeout=max(0, deadline - time.monotonic()))
            for p, _a in processes[:-1]:
                p.wait(timeout=max(0, deadline - time.monotonic()))
            output.append(raw)
            status = processes[-1][0].returncode
            if status != 0:
                out = b"".join(output).decode("utf-8", "replace").strip()
                return None, out, "derive-exit-%d" % status
            for p, argv in processes[:-1]:
                rc = p.returncode
                if rule == "base":
                    bad = rc > 1
                else:
                    bad = rc > 0 and not (os.path.basename(argv[0]) == "grep" and rc == 1)
                if bad:
                    out = b"".join(output).decode("utf-8", "replace").strip()
                    return None, out, "derive-upstream-exit-%d" % rc
        except subprocess.TimeoutExpired:
            return None, "", "derive-timeout"
        except (OSError, ValueError) as e:
            return None, "", "derive-exec-error-%s" % type(e).__name__
        finally:
            for p, _a in processes:
                if p.poll() is None:
                    p.kill()
            for p, _a in processes:
                p.wait()
                if p.stdout is not None:
                    p.stdout.close()
            for f in files:
                f.close()
    out = b"".join(output).decode("utf-8", "replace").strip()
    if not out:
        return None, out, "derive-empty"
    return out, out, None


def verdict(rule, derive, root=WORK):
    plan = fa.parse_derive(root, derive)
    if plan is None:
        return "REFUSED", ""
    derived, _raw, err = run_derive_rule(plan, root, rule)
    if err is not None:
        return "stale", err
    return "ok", derived


CASES = [
    # id, derive, base-want, note
    ("cat-missing-wc", "cat missing.txt | wc -l", "0", "upstream cat missing exit1"),
    ("cat-partial-wc", "cat d_exist.txt missing.txt | wc -l", "1", "partial output then exit1"),
    ("cut-missing-wc", "cut -d' ' -f1 missing.txt | wc -l", "0", "cut missing exit1"),
    ("head-missing-wc", "head missing.txt | wc -l", "0", "head missing exit1"),
    ("tail-missing-wc", "tail missing.txt | wc -l", "0", "tail missing exit1"),
    ("ls-missing-wc", "ls missing.txt | wc -l", "0", "ls missing exit2 (base already stale)"),
    ("sort-missing-wc", "sort missing.txt | wc -l", "0", "sort missing exit2 (base already stale)"),
    ("sha256-missing-wc", "sha256sum missing.txt | wc -l", "0", "sha256sum missing exit1"),
    ("grep-nomatch-wc", "grep absent g.txt | wc -l", "0", "grep exit1 no-match: must stay ok"),
    ("grep-count-nomatch", "grep -c absent g.txt | wc -l", "0", "grep -c exit1 no-match"),
    ("grep-warning-nomatch", "grep 'a\\d' g.txt | wc -l", "0", "grep exit1 WITH stderr warning"),
    ("grep-missing-file", "grep absent missing.txt | wc -l", "0", "grep exit2 upstream: stale"),
    ("grep-dir", "grep absent adir | wc -l", "0", "grep exit2 directory: stale"),
    ("grep-badre", "grep '[' g.txt | wc -l", "0", "grep exit2 invalid regex: stale"),
    ("success-pipe", "cat g.txt | wc -l", "1", "successful pipeline"),
    ("and-fail", "cat missing.txt && cat g.txt", "35", "&& stops on failed stage"),
    ("final-exit1-after-missing", "cat missing.txt | grep absent g.txt", "0", "final precedence over upstream"),
    ("final-cat-missing-after-grep", "grep absent g.txt | cat missing.txt", "0", "final exit1 after grep no-match"),
    ("final-python7-after-upstream", "cat missing.txt | python3 corpus/instruments/fail7.py", "0", "final exit7 precedence"),
    ("python-exit1-counter", "python3 corpus/instruments/exit1count.py | wc -l", "1", "counter exit1 with output"),
    ("python-exit1-after-output-raise", "python3 corpus/instruments/nonzero-after-output.py | wc -l", "1", "uncaught exception after output"),
    ("python-sigkill-partial", "python3 corpus/instruments/sigkill-partial.py | wc -l", "3", "negative signal upstream, partial output"),
    ("sha256-check-fail", "sha256sum -c sums.txt | grep -c OK", "1", "sha256sum -c with one FAILED: legit exit1 non-grep"),
    ("sha256-check-ok", "sha256sum -c sums-ok.txt | wc -l", "1", "sha256sum -c success"),
    ("sort-check-disorder", "sort -c unsorted.txt | wc -l", "0", "sort -c disorder exit1 non-grep"),
    ("sort-check-sorted", "sort -c sorted.txt | wc -l", "0", "sort -c sorted exit0"),
    ("python-broken-pipe-head", "python3 corpus/instruments/bigprint.py | head -1", "line 0", "upstream python writes into closed pipe"),
    ("cat-big-head-sigpipe", "cat corpus/instruments/bigprint.py | head -1", "x", "SIGPIPE negative upstream of head"),
]


def main():
    print("run_utc=%s" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    print("%-30s %-18s %-30s %-30s" % ("id", "want(base)", "BASE verdict", "CAND verdict"))
    for cid, derive, want, note in CASES:
        bv, bo = verdict("base", derive)
        cv, co = verdict("cand", derive)
        bsum = "%s %s" % (bv, bo if bv == "ok" else bo)
        csum = "%s %s" % (cv, co)
        print("%-30s %-18s %-30s %-30s  # %s" % (cid, want, bsum[:30], csum[:30], note))
        print("    derive: %s" % derive)


if __name__ == "__main__":
    main()
