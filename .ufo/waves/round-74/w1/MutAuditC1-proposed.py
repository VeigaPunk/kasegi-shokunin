"""proposed.py COUNTER — candidate fixtures for the survivors M8b, M9p, M10p, M12p.
Scratch-only; prints one FIXTURE line per case and exit = failure count. TMPDIR must be set."""
import contextlib
import importlib.util
import io
import os
import sys
import tempfile

path = sys.argv[1]
spec = importlib.util.spec_from_file_location("counter_under_test", path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

TMP = os.environ["TMPDIR"]
work = tempfile.mkdtemp(prefix="proposed-", dir=TMP)
TMPREAL = os.path.realpath(tempfile.gettempdir())
failures = 0


def tree(name, entries):
    root = os.path.join(work, name)
    kdir = os.path.join(root, "corpus", "knowledge")
    os.makedirs(kdir)
    for fn, body in entries.items():
        with open(os.path.join(kdir, fn), "w", encoding="utf-8") as fh:
            fh.write("# fixture\n" + body)
    return root


def run(root, lane):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        return m.census(root, lane)


def check(tag, got, want):
    global failures
    ok = all(got.get(k) == v for k, v in want.items())
    failures += 0 if ok else 1
    print("FIXTURE %s %s got=%s want=%s" % (
        tag, "PASS" if ok else "FAIL",
        ",".join("%s=%s" % (k, got.get(k)) for k in sorted(want)),
        ",".join("%s=%s" % (k, want[k]) for k in sorted(want))))


# P-lane: a prefix that names a directory other than --lane is prefix-less.
root = tree("p-lane", {"a.md": "recheck: cd /nonexistent-other-lane && true\n"})
check("P-lane", run(root, root), {"entries": 1, "noprefix": 1})

# P-exit1: a value exiting 1 from the foreign cwd lands in exit1_foreign.
root = tree("p-exit1", {"a.md": "recheck: cd %s && false\n" % "PLACEHOLDER"})
root = tree("p-exit1b", {"a.md": "recheck: false\n"})
check("P-exit1", run(root, root), {"entries": 1, "noprefix": 1, "exit1_foreign": 1, "exit0_foreign": 0})

# P-timeout: a value exceeding TIMEOUT is counted in exit_other (-1).
m.TIMEOUT = 1
root = tree("p-timeout", {"a.md": "recheck: sleep 4\n"})
check("P-timeout", run(root, root), {"entries": 1, "exit_other": 1, "exit0_foreign": 0})
m.TIMEOUT = 120

# P-foreign: the value runs in a fresh scratch under TMPDIR, not in the lane.
root = tree("p-foreign", {"a.md": 'recheck: case "$(pwd -P)" in "%s"/recheck-cwd-*) exit 0;; *) exit 3;; esac\n' % TMPREAL})
check("P-foreign", run(root, root), {"entries": 1, "noprefix": 1, "exit0_foreign": 1, "exit_other": 0})

print("proposed counter=%s failures=%d" % (os.path.basename(path), failures))
sys.exit(failures)
