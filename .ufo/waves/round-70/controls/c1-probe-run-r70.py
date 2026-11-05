#!/usr/bin/env python3
"""Round-70 C1 counter: the derive gate must refuse the python-head write/exec/ingress options
that the round-68 wave measured open (RevengerC1 rows 2 and 7,
`.ufo/waves/round-68/w1/RevengerC1.md`).

Frozen predicate (claims.json): on the gate named by --gate, `VERIFY measurements=12 failures=0`
and process exit 0.  The twelve measurements are

  P1 python-root-space     `python3 corpus/instruments/frontier-recheck-count.py --root .`
  P2 python-root-equals    `... --root=.`
  P3 python-root-abbrev    `... --ro .`            (argparse unique-prefix abbreviation)
  P4 python-out-space      `python3 corpus/instruments/capture-source.py --id x --url file://SRC
                            --out ABS --kind text`
  P5 python-out-equals     `... --out=ABS ...`
  P6 python-out-abbrev     `... --ou ABS ...`
  P7 python-json-space     `python3 corpus/instruments/frontier-recheck-count.py --json ABS`
      each: refused at parse time (exit 2, stderr reason=derive-not-read-only); the exec payload
      named by the fixture entry's `recheck:` line gains no marker line and the named output file
      is not created.
  8  read-only-controls-admitted   eight legitimate derives (python counter, a counter receiving a
                                    post-`--` dash operand, cat, grep -c, sort, cut, git show blob,
                                    git cat-file -t) still run and re-derive their exact value
                                    (positive controls: a blanket refusal fails here).
  9  selftest             `<gate> --selftest` exits 0 with `selftest cases=96 failures=0`.
  10 mutbat               the committed mutant battery exits 0 against <gate>.
  11 real-ledger          the committed lane ledger re-derives `figures=35 ok=35 stale=0`.
  12 no-write-side-effect the fixture trees (including the fixture .git) are byte-identical before
                          and after every run and every program marker is at 0.

Pointed at the BASE gate bytes (round-69 tip `e7c02bd`, gate sha256 `c09b0fb1…`) this same counter
is the do-nothing control: P1..P7 are admitted, P1/P2/P3 run the fixture entry's `recheck:` payload
through `bash -c`, P4/P5/P6 write their outside file and P7 writes its JSON receipt; the selftest
pins 86 cases; the write-side-effect measurement fails on the exec marker.

Usage:
  python3 .ufo/waves/round-70/controls/c1-probe-run-r70.py --gate PATH --work DIR [--lane DIR]
                                                          [--mode candidate|base|forgery]

--work must be an owned scratch directory under $HYAKU_SCRATCH: the counter builds its fixtures
there and writes nothing outside it.  Host binaries matter: results are for the `sort`, `git` and
`python3` this counter resolves on PATH; the receipt header records their versions.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

EXPECTED_SELFTEST = "selftest cases=96 failures=0"


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


def build_fixture(work, lane):
    """A miniature lane root holding the two real counters and one frontier entry.

    The entry's `recheck:` line is a valid recheck invocation that first appends to the exec
    marker, which is exactly the shape `frontier-recheck-count.py:269` runs through `bash -c`
    with cwd=root.
    """
    fixture = os.path.join(work, "fixture")
    repo = os.path.join(work, "repo")
    outside = os.path.join(work, "outside")
    for d in (fixture, repo, outside):
        if os.path.isdir(d):
            shutil.rmtree(d)
        os.makedirs(d)
    inst = os.path.join(fixture, "corpus", "instruments")
    os.makedirs(inst)
    for name in ("frontier-recheck-count.py", "capture-source.py"):
        shutil.copyfile(os.path.join(lane, "corpus", "instruments", name),
                        os.path.join(inst, name))
    with open(os.path.join(inst, "ok.py"), "w", encoding="utf-8", newline="\n") as f:
        f.write("print(35)\n")
    with open(os.path.join(inst, "source-recheck.py"), "w", encoding="utf-8", newline="\n") as f:
        f.write("print('source-recheck fixture ok')\n")
    os.makedirs(os.path.join(fixture, "corpus", "knowledge"))
    os.makedirs(os.path.join(fixture, "corpus", "source-snapshots", "fix"))
    with open(os.path.join(fixture, "corpus", "source-snapshots", "fix", "manifest.json"),
              "w", encoding="utf-8", newline="\n") as f:
        json.dump({"schema_version": 1, "purpose": "r70 exec fixture",
                   "sources": [{"id": "S001"}]}, f)
        f.write("\n")
    with open(os.path.join(fixture, "corpus", "README.md"), "w", encoding="utf-8",
              newline="\n") as f:
        f.write("| id | topic | status | entry | sources | next |\n")
        f.write("|---|---|---|---|---|---|\n")
        f.write("| F01 | fixture | admitted | knowledge/x.md | S001 | fixture row |\n")
    mark = os.path.join(work, "marker.exec")
    with open(os.path.join(fixture, "corpus", "knowledge", "x.md"), "w", encoding="utf-8",
              newline="\n") as f:
        f.write("# fixture entry\n\n")
        f.write("source: S001\n\n")
        f.write("Ground: S001 is cited here as fixture evidence.\n\n")
        f.write("recheck: printf 'ran\\n' >> %s; python3 -I corpus/instruments/"
                "source-recheck.py --manifest corpus/source-snapshots/fix/manifest.json "
                "--source S001\n" % mark)
    with open(os.path.join(fixture, "src.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("fixture source bytes\n")
    with open(os.path.join(fixture, "g.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("35\n")
    with open(os.path.join(repo, "g.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("35\n")
    git = ["git", "-C", repo]
    rc, out, err = run(git + ["init", "-q", "."], work)
    if rc != 0:
        raise SystemExit("fixture git init failed rc=%d %s" % (rc, err))
    rc, out, _ = run(git + ["rev-parse", "--show-toplevel"], work)
    if rc != 0 or os.path.realpath(out.strip()) != os.path.realpath(repo):
        raise SystemExit("fixture toplevel mismatch: %r" % out.strip())
    identity = ["-c", "user.email=fixture@shokunin.local", "-c", "user.name=fixture"]
    for argv in (git + ["add", "-A"], git + identity + ["commit", "-qm", "fixture commit"]):
        rc, _, err = run(argv, work)
        if rc != 0:
            raise SystemExit("fixture git %s failed rc=%d %s" % (argv[-1], rc, err))
    return fixture, repo, outside, mark


def probe(work, gate, root, name, derive, want, env):
    ledger = os.path.join(work, name + ".json")
    with open(ledger, "w", encoding="utf-8") as f:
        json.dump({"figures": [{"id": name, "record": "fixture:1", "recorded": want,
                                "derive": derive, "want": want}]}, f)
    return run([sys.executable, gate, "--ledger", ledger, "--root", root], work, env=env)


def tool_versions():
    out = []
    for argv in (["sort", "--version"], ["git", "--version"], [sys.executable, "--version"]):
        try:
            rc, o, e = run(argv, "/")
            out.append(((o or e).strip().splitlines() or ["?"])[0])
        except OSError as exc:
            out.append("%s unavailable %s" % (argv[0], exc))
    return "; ".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="kasegi r70 C1 python-head option counter")
    ap.add_argument("--gate", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--lane", default="/home/vgpnk/Projects/shokunin/kasegi-shokunin")
    ap.add_argument("--mode", default="candidate", choices=("candidate", "base", "forgery"))
    ap.add_argument("--timeout", type=int, default=900)
    a = ap.parse_args(argv)

    gate = os.path.abspath(a.gate)
    work = os.path.abspath(a.work)
    lane = os.path.abspath(a.lane)
    if not os.path.isfile(gate):
        print("UNAVAILABLE reason=gate-missing path=%s" % gate)
        return 2
    os.makedirs(work, exist_ok=True)
    print("HOST %s" % tool_versions())

    fixture, repo, outside, exec_mark = build_fixture(work, lane)
    open(exec_mark, "w").close()
    env = dict(os.environ)
    env["TMPDIR"] = work
    env["HYAKU_SCRATCH"] = work

    before = tree_state(fixture) + tree_state(repo)
    rows = []

    def record(name, ok, detail):
        rows.append((name, ok, detail))
        print("MEASURE %s %s %s" % (name, "ok" if ok else "FAIL", detail))

    src = os.path.join(fixture, "src.txt")
    counter = "corpus/instruments/frontier-recheck-count.py"
    capture = "corpus/instruments/capture-source.py"
    probes = [
        ("python-root-space", fixture,
         "python3 %s --root ." % counter, "1", None),
        ("python-root-equals", fixture,
         "python3 %s --root=." % counter, "1", None),
        ("python-root-abbrev", fixture,
         "python3 %s --ro ." % counter, "1", None),
        ("python-out-space", fixture,
         "python3 %s --id x --url file://%s --out %s --kind text"
         % (capture, src, os.path.join(outside, "p4.txt")), "fixture", None),
        ("python-out-equals", fixture,
         "python3 %s --id x --url file://%s --out=%s --kind text"
         % (capture, src, os.path.join(outside, "p5.txt")), "fixture", None),
        ("python-out-abbrev", fixture,
         "python3 %s --id x --url file://%s --ou %s --kind text"
         % (capture, src, os.path.join(outside, "p6.txt")), "fixture", None),
        ("python-json-space", fixture,
         "python3 %s --json %s" % (counter, os.path.join(outside, "p7.json")), "1", None),
    ]
    for i, (name, root, derive, want, _unused) in enumerate(probes, 1):
        outfile = None
        for cand in ("p4.txt", "p5.txt", "p6.txt", "p7.json"):
            if cand in derive:
                outfile = os.path.join(outside, cand)
        start = marker_lines(exec_mark)
        rc, out, err = probe(work, gate, root, "p%d" % i, derive, want, env)
        ran = marker_lines(exec_mark) - start
        wrote = os.path.exists(outfile) if outfile else False
        refused = rc == 2 and "reason=derive-not-read-only" in err
        record("P%d-%s" % (i, name), refused and ran == 0 and not wrote,
               "rc=%d refused=%d marker_runs=%d wrote=%d"
               % (rc, int(refused), ran, int(wrote)))

    controls = [
        ("python3 corpus/instruments/ok.py", fixture, "35"),
        ("python3 corpus/instruments/ok.py -- --root", fixture, "35"),
        ("cat g.txt", fixture, "35"),
        ("grep -c 35 g.txt", fixture, "1"),
        ("sort g.txt | head -n 1", fixture, "35"),
        ("cut -c1-2 g.txt | head -n 1", fixture, "35"),
        ("git show HEAD:g.txt | head -n 1", repo, "35"),
        ("git cat-file -t HEAD", repo, "commit"),
    ]
    bad = []
    for i, (derive, root, want) in enumerate(controls):
        rc, out, err = probe(work, gate, root, "c%d" % i, derive, want, env)
        if rc != 0:
            bad.append("%s rc=%d" % (derive, rc))
    record("read-only-controls-admitted", not bad,
           "controls=%d failed=%d%s" % (len(controls), len(bad),
                                        (" " + ";".join(bad)) if bad else ""))

    rc, out, err = run([sys.executable, gate, "--selftest"], lane, env=env, timeout=a.timeout)
    tail = [ln for ln in out.splitlines() if ln.startswith("selftest cases=")]
    record("selftest", rc == 0 and bool(tail) and tail[-1] == EXPECTED_SELFTEST,
           "%s rc=%d" % (tail[-1] if tail else "no-cases-line", rc))

    mutbat = os.path.join(lane, "corpus", "instruments", "figure-audit-mutbat.py")
    rc, out, err = run([sys.executable, mutbat, "--instrument", gate], work, env=env,
                       timeout=a.timeout)
    record("mutbat", rc == 0,
           "rc=%d %s" % (rc, (out.strip().splitlines() or ["no-output"])[-1][:120]))

    ledger = os.path.join(lane, "corpus", "instruments", "figure-audit-ledger.json")
    rc, out, err = run([sys.executable, gate, "--ledger", ledger, "--root", lane], lane, env=env,
                       timeout=a.timeout)
    line = [ln for ln in out.splitlines() if ln.startswith("FIGURE-AUDIT")]
    record("real-ledger", rc == 0 and bool(line) and "figures=35 ok=35 stale=0" in line[-1],
           "%s rc=%d" % (line[-1] if line else "no-audit-line", rc))

    after = tree_state(fixture) + tree_state(repo)
    runs = marker_lines(exec_mark)
    record("no-write-side-effect", before == after and runs == 0,
           "fixture_changed=%d marker_runs=%d" % (0 if before == after else 1, runs))

    failures = sum(1 for _, ok, _ in rows if not ok)
    print("VERIFY measurements=%d failures=%d gate_sha256=%s mode=%s"
          % (len(rows), failures, sha256_file(gate), a.mode))
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
