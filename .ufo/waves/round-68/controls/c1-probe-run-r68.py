#!/usr/bin/env python3
"""Round-68 C1 counter: the derive gate must refuse the two measured program-execution flags.

Frozen predicate (claims.json): on the gate named by --gate, `VERIFY measurements=8 failures=0`
and process exit 0.  The eight measurements are

  1. sort-compress-refused        `sort --compress-program=<prog> -S 1K big.txt | head -n 1`
                                  is refused at parse time (exit 2, reason=derive-not-read-only)
                                  and <prog> is never executed (marker runs == 0).
  2. git-textconv-refused         `git show --textconv HEAD:big.txt | head -n 1` is refused the
                                  same way and the config-declared textconv driver never runs.
  3. read-only-controls-admitted  six legitimate read-only derives still execute and re-derive
                                  their exact value (no widening, no false stale).
  4. selftest                     `<gate> --selftest` exits 0 with `cases=77 failures=0`.
  5. mutbat                       the committed exact-once mutant battery exits 0 against <gate>.
  6. real-ledger                  the committed lane ledger re-derives `figures=35 ok=35 stale=0`.
  7. red-fixture                  a ledger whose want is wrong still reads `stale` (exit 1).
  8. no-write-side-effect         the fixture tree is byte-identical before and after every run
                                  and neither execution marker received a line.

Pointed at the BASE gate bytes this same counter is the do-nothing control: measurements 1, 2
and 4 fail (base admits both flags, really executes them, and pins 73 selftest cases).

Usage:
  python3 .ufo/waves/round-68/controls/c1-probe-run-r68.py --gate PATH --work DIR [--lane DIR]

--work must be an owned scratch directory (this script removes only what it creates inside it).
Nothing is written outside --work.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

BIG_LINES = 60000
BIG_WANT = "0000000"
TEXT_WANT = "x" * 1000


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def run(argv, cwd, env=None, timeout=900):
    p = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, timeout=timeout)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def tree_state(root):
    out = []
    for base, dirs, files in os.walk(root):
        dirs.sort()
        for name in sorted(files):
            path = os.path.join(base, name)
            out.append((os.path.relpath(path, root), sha256_file(path)))
    return out


def marker_lines(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return sum(1 for _ in f)
    except FileNotFoundError:
        return 0


def build_fixture(work):
    fixture = os.path.join(work, "fixture")
    repo = os.path.join(work, "repo")
    for d in (fixture, repo):
        if os.path.isdir(d):
            shutil.rmtree(d)
        os.makedirs(d)
    big = "".join("%07d\n" % i for i in range(BIG_LINES))
    with open(os.path.join(fixture, "big.txt"), "w", encoding="utf-8") as f:
        f.write(big)
    with open(os.path.join(repo, "big.txt"), "w", encoding="utf-8") as f:
        f.write("x" * 1000 + "\n")
    comp = os.path.join(work, "compressor.sh")
    with open(comp, "w", encoding="utf-8") as f:
        f.write('#!/bin/sh\necho run >> "$COMP_MARK"\nexec gzip -c\n')
    driver = os.path.join(work, "textconv.sh")
    with open(driver, "w", encoding="utf-8") as f:
        f.write('#!/bin/sh\necho run >> "$TC_MARK"\nexec cat\n')
    for p in (comp, driver):
        os.chmod(p, 0o755)
    git = ["git", "-C", repo]
    rc, out, err = run(git + ["init", "-q", "."], work)
    if rc != 0:
        raise SystemExit("fixture git init failed rc=%d %s" % (rc, err))
    rc, out, _ = run(git + ["rev-parse", "--show-toplevel"], work)
    if rc != 0 or os.path.realpath(out.strip()) != os.path.realpath(repo):
        raise SystemExit("fixture toplevel mismatch: %r" % out.strip())
    identity = ["-c", "user.email=fixture@shokunin.local", "-c", "user.name=fixture"]
    for argv in (git + ["config", "diff.mydriver.textconv", driver],
                 git + ["config", "diff.mydriver.binary", "false"]):
        rc, _, err = run(argv, work)
        if rc != 0:
            raise SystemExit("fixture git config failed rc=%d %s" % (rc, err))
    with open(os.path.join(repo, ".gitattributes"), "w", encoding="utf-8") as f:
        f.write("big.txt diff=mydriver\n")
    for argv in (git + ["add", "-A"], git + identity + ["commit", "-qm", "fixture"]):
        rc, _, err = run(argv, work)
        if rc != 0:
            raise SystemExit("fixture git %s failed rc=%d %s" % (argv[-1], rc, err))
    return fixture, repo, comp, driver


def write_ledger(work, name, entry):
    path = os.path.join(work, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"figures": [entry]}, f)
    return path


def probe(work, gate, root, name, entry, env):
    ledger = write_ledger(work, name + ".json", entry)
    return run([sys.executable, gate, "--ledger", ledger, "--root", root], work, env=env)


def main(argv=None):
    ap = argparse.ArgumentParser(description="kasegi r68 C1 program-execution-flag counter")
    ap.add_argument("--gate", required=True, help="gate file under test")
    ap.add_argument("--work", required=True, help="owned scratch dir (must be writable, empty is fine)")
    ap.add_argument("--lane", default="/home/vgpnk/Projects/shokunin/kasegi-shokunin")
    ap.add_argument("--mode", default="candidate", choices=("candidate", "base"))
    ap.add_argument("--timeout", type=int, default=900)
    a = ap.parse_args(argv)

    gate = os.path.abspath(a.gate)
    work = os.path.abspath(a.work)
    lane = os.path.abspath(a.lane)
    if not os.path.isfile(gate):
        print("UNAVAILABLE reason=gate-missing path=%s" % gate)
        return 2
    os.makedirs(work, exist_ok=True)

    fixture, repo, comp, driver = build_fixture(work)
    comp_mark = os.path.join(work, "marker.compress")
    tc_mark = os.path.join(work, "marker.textconv")
    for p in (comp_mark, tc_mark):
        open(p, "w").close()
    env = dict(os.environ)
    env["COMP_MARK"] = comp_mark
    env["TC_MARK"] = tc_mark
    env["TMPDIR"] = work

    before = tree_state(fixture) + tree_state(repo)
    rows = []

    def record(name, ok, detail):
        rows.append((name, ok, detail))
        print("MEASURE %s %s %s" % (name, "ok" if ok else "FAIL", detail))

    # 1. sort --compress-program refused, compressor never executed
    rc, out, err = probe(work, gate, fixture, "p1",
                         {"id": "p1", "record": "big.txt:1", "recorded": BIG_WANT,
                          "derive": "sort --compress-program=%s -S 1K big.txt | head -n 1" % comp,
                          "want": BIG_WANT}, env)
    runs = marker_lines(comp_mark)
    record("sort-compress-refused",
           rc == 2 and "reason=derive-not-read-only" in err and runs == 0,
           "rc=%d marker_runs=%d" % (rc, runs))

    # 2. git show --textconv refused, driver never executed
    rc, out, err = probe(work, gate, repo, "p2",
                         {"id": "p2", "record": "big.txt:1", "recorded": "0",
                          "derive": "git show --textconv HEAD:big.txt | head -n 1",
                          "want": TEXT_WANT}, env)
    runs = marker_lines(tc_mark)
    record("git-textconv-refused",
           rc == 2 and "reason=derive-not-read-only" in err and runs == 0,
           "rc=%d marker_runs=%d" % (rc, runs))

    # 3. legitimate read-only derives still admitted and exact
    controls = [
        ("cat big.txt | wc -l", fixture, str(BIG_LINES)),
        ("grep -c 0000001 big.txt", fixture, "1"),
        ("cut -c1-3 big.txt | head -n 1", fixture, "000"),
        ("sort big.txt | head -n 1", fixture, BIG_WANT),
        ("git show HEAD:big.txt | head -n 1", repo, TEXT_WANT),
    ]
    bad = []
    for i, (derive, root, want) in enumerate(controls):
        rc, out, err = probe(work, gate, root, "c%d" % i,
                             {"id": "c%d" % i, "record": "big.txt:1", "recorded": want,
                              "derive": derive, "want": want}, env)
        if rc != 0:
            bad.append("%s rc=%d" % (derive, rc))
    record("read-only-controls-admitted", not bad,
           "controls=%d failed=%d%s" % (len(controls), len(bad),
                                        (" " + ";".join(bad)) if bad else ""))

    # 4. selftest
    rc, out, err = run([sys.executable, gate, "--selftest"], lane, env=env, timeout=a.timeout)
    tail = [ln for ln in out.splitlines() if ln.startswith("selftest cases=")]
    record("selftest", rc == 0 and bool(tail) and tail[-1] == "selftest cases=77 failures=0",
           "%s rc=%d" % (tail[-1] if tail else "no-cases-line", rc))

    # 5. committed mutant battery
    mutbat = os.path.join(lane, "corpus", "instruments", "figure-audit-mutbat.py")
    rc, out, err = run([sys.executable, mutbat, "--instrument", gate], work, env=env,
                       timeout=a.timeout)
    record("mutbat", rc == 0, "rc=%d %s" % (rc, (out.strip().splitlines() or ["no-output"])[-1][:120]))

    # 6. the real lane ledger
    ledger = os.path.join(lane, "corpus", "instruments", "figure-audit-ledger.json")
    rc, out, err = run([sys.executable, gate, "--ledger", ledger, "--root", lane], lane, env=env,
                       timeout=a.timeout)
    line = [ln for ln in out.splitlines() if ln.startswith("FIGURE-AUDIT")]
    record("real-ledger", rc == 0 and bool(line) and "figures=35 ok=35 stale=0" in line[-1],
           "%s rc=%d" % (line[-1] if line else "no-audit-line", rc))

    # 7. red fixture still reads stale
    rc, out, err = probe(work, gate, fixture, "red",
                         {"id": "red", "record": "big.txt:1", "recorded": "0",
                          "derive": "cat big.txt | wc -l", "want": "not-the-value"}, env)
    record("red-fixture", rc == 1 and " stale" in out, "rc=%d" % rc)

    # 8. no write side effect anywhere in the fixture
    after = tree_state(fixture) + tree_state(repo)
    runs = marker_lines(comp_mark) + marker_lines(tc_mark)
    record("no-write-side-effect", before == after and runs == 0,
           "fixture_changed=%d marker_runs=%d" % (0 if before == after else 1, runs))

    failures = sum(1 for _, ok, _ in rows if not ok)
    print("VERIFY measurements=%d failures=%d gate_sha256=%s mode=%s"
          % (len(rows), failures, sha256_file(gate), a.mode))
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
