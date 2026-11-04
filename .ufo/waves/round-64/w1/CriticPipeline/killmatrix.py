#!/usr/bin/env python3
"""Kill matrix: candidate intended rule plus plausible mis-implementations.

Each mutant is a (name, decide, precedence) triple. `decide(stage_index, argvs, rc)` returns
the upstream reason string or None. `precedence` is 'final-first' (spec) or 'upstream-first'.
Expected verdict per probe is the intended outcome; a mutant is KILLED by a probe if its
verdict/reason differs from the expectation.
"""
import importlib.util
import os
import subprocess
import tempfile
import time

BASE = "/fast/scratch/hyaku/kasegi-r64/CriticPipeline/base/figure-audit.py"
WORK = "/fast/scratch/hyaku/kasegi-r64/CriticPipeline/work"
spec = importlib.util.spec_from_file_location("fa", BASE)
fa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fa)


def is_grep(argv):
    return os.path.basename(argv[0]) == "grep"


def d_intended(i, argvs, rc):
    if rc > 0 and not (is_grep(argvs[i]) and rc == 1):
        return "derive-upstream-exit-%d" % rc
    return None


def d_misidx(i, argvs, rc):  # exemption keyed to the NEXT stage's argv (off-by-one)
    nxt = argvs[i + 1] if i + 1 < len(argvs) else argvs[i]
    if rc > 0 and not (is_grep(nxt) and rc == 1):
        return "derive-upstream-exit-%d" % rc
    return None


def d_anygrep(i, argvs, rc):  # exemption if ANY stage in pipeline is grep
    if rc > 0 and not (any(is_grep(a) for a in argvs) and rc == 1):
        return "derive-upstream-exit-%d" % rc
    return None


def d_substr(i, argvs, rc):  # exemption by substring match on whole argv
    if rc > 0 and not ("grep" in " ".join(argvs[i]) and rc == 1):
        return "derive-upstream-exit-%d" % rc
    return None


def d_negstale(i, argvs, rc):  # any nonzero incl. signals is stale
    if rc != 0 and not (is_grep(argvs[i]) and rc == 1):
        return "derive-upstream-exit-%d" % rc
    return None


def d_sigpipe_only(i, argvs, rc):  # option: ignore only SIGPIPE (-13) upstream, other signals stale
    if rc < 0 and rc != -13:
        return "derive-upstream-exit-%d" % rc
    if rc > 0 and not (is_grep(argvs[i]) and rc == 1):
        return "derive-upstream-exit-%d" % rc
    return None


def d_rc1any(i, argvs, rc):  # ignore all upstream exit1 (base behaviour for rc1)
    if rc > 1:
        return "derive-upstream-exit-%d" % rc
    return None


MUTANTS = [
    ("intended", d_intended, "final-first"),
    ("mut-misidx-next-argv", d_misidx, "final-first"),
    ("mut-any-grep-in-pipe", d_anygrep, "final-first"),
    ("mut-substring-grep", d_substr, "final-first"),
    ("mut-negative-stale", d_negstale, "final-first"),
    ("opt-sigpipe-only-negatives", d_sigpipe_only, "final-first"),
    ("mut-base-rc1-ignored", d_rc1any, "final-first"),
    ("mut-upstream-before-final", d_intended, "upstream-first"),
]


def run(plan, root, decide, precedence):
    output = []
    deadline = time.monotonic() + 300
    for pipeline in plan:
        processes, files = [], []
        previous = None
        try:
            for argv, input_path in pipeline:
                stdin = previous
                if input_path is not None:
                    stdin = open(os.path.join(root, input_path), "rb")
                    files.append(stdin)
                errors = tempfile.TemporaryFile()
                files.append(errors)
                p = subprocess.Popen(argv, cwd=root, stdin=stdin,
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
            argvs = [a for _p, a in processes]

            def upstream_reason():
                for i, (p, _a) in enumerate(processes[:-1]):
                    r = decide(i, argvs, p.returncode)
                    if r:
                        return r
                return None

            if precedence == "upstream-first":
                r = upstream_reason()
                if r:
                    return None, r
            if status != 0:
                return None, "derive-exit-%d" % status
            r = upstream_reason()
            if r:
                return None, r
        except subprocess.TimeoutExpired:
            return None, "derive-timeout"
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
        return None, "derive-empty"
    return out, None


# probe id, derive, expected verdict ("ok:<value>" or "stale:<reason>")
PROBES = [
    ("cat-missing", "cat missing.txt | wc -l", "stale:derive-upstream-exit-1"),
    ("cat-partial", "cat d_exist.txt missing.txt | wc -l", "stale:derive-upstream-exit-1"),
    ("cut-missing", "cut -d' ' -f1 missing.txt | wc -l", "stale:derive-upstream-exit-1"),
    ("head-missing", "head missing.txt | wc -l", "stale:derive-upstream-exit-1"),
    ("tail-missing", "tail missing.txt | wc -l", "stale:derive-upstream-exit-1"),
    ("ls-missing", "ls missing.txt | wc -l", "stale:derive-upstream-exit-2"),
    ("sort-missing", "sort missing.txt | wc -l", "stale:derive-upstream-exit-2"),
    ("sha256-missing", "sha256sum missing.txt | wc -l", "stale:derive-upstream-exit-1"),
    ("grep-nomatch", "grep absent g.txt | wc -l", "ok:0"),
    ("grep-nomatch-warning", "grep 'a\\d' g.txt | wc -l", "ok:0"),
    ("grep-missing-exit2", "grep absent missing.txt | wc -l", "stale:derive-upstream-exit-2"),
    ("mid-cat-missing-grep", "cat missing.txt | grep absent g.txt | wc -l", "stale:derive-upstream-exit-1"),
    ("grep-then-cat-missing", "grep absent g.txt | cat missing.txt | wc -l", "stale:derive-upstream-exit-1"),
    ("grep-nomatch-chain", "grep absent g.txt | grep absent | wc -l", "ok:0"),
    ("and-second-pipe-cat-missing", "grep absent g.txt | wc -l && cat missing.txt | wc -l", "stale:derive-upstream-exit-1"),
    ("filename-contains-grep", "cat grep-missing.txt | wc -l", "stale:derive-upstream-exit-1"),
    ("final-python7-precedence", "cat missing.txt | python3 corpus/instruments/fail7.py", "stale:derive-exit-7"),
    ("final-grep1-precedence", "cat missing.txt | grep absent g.txt", "stale:derive-exit-1"),
    ("sigpipe-head", "cat big.txt | head -1", "ok:row 0 value"),
    ("sigpipe-grep-head", "grep row big.txt | head -1", "ok:row 0 value"),
    ("success", "cat g.txt | wc -l", "ok:1"),
    ("negative-signal-counter", "python3 corpus/instruments/sigkill-partial.py | wc -l", "ok:3"),
    ("sha256-check-fail", "sha256sum -c sums.txt | grep -c OK", "stale:derive-upstream-exit-1"),
    ("sort-check-disorder", "sort -c unsorted.txt | wc -l", "stale:derive-upstream-exit-1"),
    ("python-exit1-counter", "python3 corpus/instruments/exit1count.py | wc -l", "stale:derive-upstream-exit-1"),
    ("python-brokenpipe-head", "python3 corpus/instruments/bigprint.py | head -1", "stale:derive-upstream-exit-1"),
]


def main():
    print("run_utc=%s" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    results = {}
    for mname, decide, prec in MUTANTS:
        killed = []
        for pid, derive, expect in PROBES:
            plan = fa.parse_derive(WORK, derive)
            assert plan is not None, derive
            out, err = run(plan, WORK, decide, prec)
            got = ("ok:%s" % out) if err is None else ("stale:%s" % err)
            if got != expect:
                killed.append((pid, expect, got))
        results[mname] = killed
        print("MUTANT %-28s killed_by=%d" % (mname, len(killed)))
        for pid, exp, got in killed:
            print("    %-28s want=%-30s got=%s" % (pid, exp, got))


if __name__ == "__main__":
    main()
