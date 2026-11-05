"""Survivor fixture driver (scratch only). Usage: TMPDIR=<dir> python3 fixtures.py <counter.py>

Loads a counter module by path and runs proposed selftest fixtures against it. Each fixture
prints PASS (module behaves as the spec says) or FAIL (module deviates). Exit = failure count.
The caller must start with an empty TMPDIR: F-leak counts recheck-cwd-* leftovers under it.
"""
import contextlib
import glob
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
work = tempfile.mkdtemp(prefix="fixture-", dir=TMP)
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


def census(root, lane):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        counts = m.census(root, lane)
    return counts


def check(tag, got, want):
    global failures
    ok = all(got.get(k) == v for k, v in want.items())
    if not ok:
        failures += 1
    print("FIXTURE %s %s got=%s want=%s" % (
        tag, "PASS" if ok else "FAIL",
        ",".join("%s=%s" % (k, got.get(k)) for k in sorted(want)),
        ",".join("%s=%s" % (k, want[k]) for k in sorted(want))))


# F-foreign (kills M3, M5): the recheck must run in a fresh scratch dir under TMPDIR.
# Entry is prefix-less on purpose: the check runs from the foreign cwd only.
root = tree("f-foreign", {"a.md": 'recheck: case "$(pwd -P)" in "%s"/recheck-cwd-*) exit 0;; *) exit 3;; esac\n' % TMPREAL})
check("F-foreign", census(root, root),
      {"entries": 1, "noprefix": 1, "exit0_foreign": 1, "exit_other": 0})

# F-leak (kills M6): after the census above, no recheck-cwd-* scratch may remain under TMPDIR.
leftover = glob.glob(os.path.join(TMP, "recheck-cwd-*"))
check("F-leak", {"leftover": len(leftover)}, {"leftover": 0})

# F-first (kills M7 last-line variant and the first-AND-last reading): only the FIRST
# recheck line is the entry's value; the second, prefix-less exit-2 line must not count.
lane_first = os.path.join(work, "f-first")
root = tree("f-first", {"b.md": "recheck: cd %s && true\nrecheck: python3 corpus/instruments/absent.py\n"
                        % lane_first})
check("F-first", census(root, lane_first),
      {"entries": 1, "noprefix": 0, "exit2_foreign": 0, "exit0_foreign": 1})

# F-lane (kills M8): with --lane different from --root, the prefix is built from --lane.
other = os.path.join(work, "f-lane-other")
os.makedirs(other)
root = tree("f-lane", {"c.md": "recheck: cd %s && true\n" % other})
check("F-lane", census(root, other),
      {"entries": 1, "noprefix": 0, "exit0_foreign": 1})

# F-result (kills M4): main() must print the RESULT line that matches its exit code.
bad = tree("f-result-bad", {"d.md": "recheck: true\n"})
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc_bad = m.main(["x", "--root", bad, "--lane", bad])
last_bad = buf.getvalue().strip().splitlines()[-1]
lane_good = os.path.join(work, "f-result-good")
good = tree("f-result-good", {"e.md": "recheck: cd %s && true\n" % lane_good})
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc_good = m.main(["x", "--root", good, "--lane", lane_good])
last_good = buf.getvalue().strip().splitlines()[-1]
check("F-result", {"rc_bad": rc_bad, "last_bad": last_bad, "rc_good": rc_good, "last_good": last_good},
      {"rc_bad": 1, "last_bad": "RECHECK-CWD-RESULT nonconformant", "rc_good": 0,
       "last_good": "RECHECK-CWD-RESULT conformant"})

print("fixtures counter=%s failures=%d" % (os.path.basename(path), failures))
sys.exit(failures)
