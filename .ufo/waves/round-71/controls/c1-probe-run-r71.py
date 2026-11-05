#!/usr/bin/env python3
"""Round-71 C1 counter: per-script python-head denial plus a fail-closed census.

The round-70 gate denied one global flag list for every python head, so ten read-only
derives the round-70 critic measured (`CriticC1` rows 2-11, `.ufo/waves/round-70/w1/`)
were refused while the exec class stayed reachable with NO option at all
(`frontier-recheck-count.py` runs a root-supplied `recheck:` payload through `bash -c`,
`--selftest` builds and commits fixture lanes in 15 instruments).  This counter measures
both directions on the same gate:

  negatives N1..N12 - must be refused at parse time (exit 2, `reason=derive-not-read-only`),
                      with no fixture write and no exec marker line:
    N1  python-root-space        frontier-recheck-count.py --root .
    N2  python-root-equals       frontier-recheck-count.py --root=.
    N3  python-root-abbrev       frontier-recheck-count.py --ro .
    N4  python-out-space         capture-source.py --out ABS
    N5  python-out-equals        capture-source.py --out=ABS
    N6  python-out-abbrev        capture-source.py --ou ABS
    N7  python-json-space        frontier-recheck-count.py --json ABS
    N8  python-no-option-head    frontier-recheck-count.py            (no option at all)
    N9  python-selftest          capture-binding-check.py --selftest
    N10 python-short-o           capture-source.py -o ABS
    N11 python-output-long       capture-source.py --output ABS
    N12 python-unknown-head      r99-unknown-probe.py                 (absent from the census)

  positives R1..R8 - the read-only derives the round-70 critic measured as over-refused;
                      each must be ADMITTED (no refusal) and, when the counter exits 0,
                      re-derive exactly the value the same command prints when run
                      directly against the lane root:
    R1  capture-binding-check.py --root .
    R2  kill-rule-check.py --root .
    R3  r44-frontier-count.py --root .
    R4  claim-package-check.py corpus/knowledge/cve-json-record-format.md --json
    R5  citation-ground-check.py --root .                 (counter exits 1 -> stale, admitted)
    R6  gate-quote-audit.py --root .                      (counter exits 1 -> stale, admitted)
    R7  r44-routed-defects.py --root .                    (counter exits 1 -> stale, admitted)
    R8  capture-binding-check.py --root . | head -n 1     (pipeline, admitted)

  plus four whole-gate measurements: selftest (pin >= --min-selftest, failures=0), the
  committed mutant battery, the real lane ledger, and the no-write-side-effect check.

Frozen predicate (claims.json): `VERIFY measurements=25 failures=0` and exit 0 on the
frozen candidate gate; the do-nothing control (the round-70 gate, sha256 7a8d52eb...)
scores at least ten failures on the same bytes and exits 1; a blanket-refusal forgery
fails every positive R1..R8 and exits 1.

Usage:
  python3 -B .ufo/waves/round-71/controls/c1-probe-run-r71.py --gate PATH --work DIR \
      [--lane DIR] [--mode candidate|donothing|base|forgery] [--min-selftest 104]

--work must be an owned scratch directory under $HYAKU_SCRATCH; the counter builds its
fixtures there and writes nothing outside it.  Host binaries matter: results are for the
`sort`, `git` and `python3` this counter resolves on PATH; the receipt header records them.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

DEFAULT_MIN_SELFTEST = 104


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
    """A miniature lane root holding the counters the negative rows name plus one frontier
    entry whose `recheck:` line appends to an exec marker before running a trivial script."""
    fixture = os.path.join(work, "fixture")
    repo = os.path.join(work, "repo")
    outside = os.path.join(work, "outside")
    for d in (fixture, repo, outside):
        if os.path.isdir(d):
            shutil.rmtree(d)
        os.makedirs(d)
    inst = os.path.join(fixture, "corpus", "instruments")
    os.makedirs(inst)
    for name in ("frontier-recheck-count.py", "capture-source.py", "capture-binding-check.py"):
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
        json.dump({"schema_version": 1, "purpose": "r71 exec fixture",
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


def refused(rc, err):
    return rc == 2 and "reason=derive-not-read-only" in err


def main(argv=None):
    ap = argparse.ArgumentParser(description="kasegi r71 C1 per-script python-head counter")
    ap.add_argument("--gate", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--lane", default="/home/vgpnk/Projects/shokunin/kasegi-shokunin")
    ap.add_argument("--mode", default="candidate",
                    choices=("candidate", "donothing", "base", "forgery"))
    ap.add_argument("--min-selftest", type=int, default=DEFAULT_MIN_SELFTEST)
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
    print("GATE sha256=%s mode=%s" % (sha256_file(gate), a.mode))

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
    negatives = [
        ("N1-python-root-space", "python3 %s --root ." % counter, None),
        ("N2-python-root-equals", "python3 %s --root=." % counter, None),
        ("N3-python-root-abbrev", "python3 %s --ro ." % counter, None),
        ("N4-python-out-space",
         "python3 %s --id x --url file://%s --out %s --kind text"
         % (capture, src, os.path.join(outside, "n4.txt")), os.path.join(outside, "n4.txt")),
        ("N5-python-out-equals",
         "python3 %s --id x --url file://%s --out=%s --kind text"
         % (capture, src, os.path.join(outside, "n5.txt")), os.path.join(outside, "n5.txt")),
        ("N6-python-out-abbrev",
         "python3 %s --id x --url file://%s --ou %s --kind text"
         % (capture, src, os.path.join(outside, "n6.txt")), os.path.join(outside, "n6.txt")),
        ("N7-python-json-space",
         "python3 %s --json %s" % (counter, os.path.join(outside, "n7.json")),
         os.path.join(outside, "n7.json")),
        ("N8-python-no-option-head", "python3 %s" % counter, None),
        ("N9-python-selftest",
         "python3 corpus/instruments/capture-binding-check.py --selftest", None),
        ("N10-python-short-o",
         "python3 %s --id x --url file://%s -o %s --kind text"
         % (capture, src, os.path.join(outside, "n10.txt")), os.path.join(outside, "n10.txt")),
        ("N11-python-output-long",
         "python3 %s --id x --url file://%s --output %s --kind text"
         % (capture, src, os.path.join(outside, "n11.txt")), os.path.join(outside, "n11.txt")),
        ("N12-python-unknown-head", "python3 corpus/instruments/r99-unknown-probe.py", None),
    ]
    for name, derive, outfile in negatives:
        start = marker_lines(exec_mark)
        rc, out, err = probe(work, gate, fixture, name.split("-")[0].lower(), derive,
                             "1", env)
        ran = marker_lines(exec_mark) - start
        wrote = os.path.exists(outfile) if outfile else False
        ok = refused(rc, err) and ran == 0 and not wrote
        record(name, ok, "rc=%d refused=%d marker_runs=%d wrote=%d"
               % (rc, int(refused(rc, err)), ran, int(wrote)))

    positives = [
        ("R1-capture-binding-root", "python3 corpus/instruments/capture-binding-check.py --root ."),
        ("R2-kill-rule-root", "python3 corpus/instruments/kill-rule-check.py --root ."),
        ("R3-frontier-count-root", "python3 corpus/instruments/r44-frontier-count.py --root ."),
        ("R4-claim-package-json",
         "python3 corpus/instruments/claim-package-check.py "
         "corpus/instruments/fixtures/claim-package/exemplar --json"),
        ("R5-citation-ground-root", "python3 corpus/instruments/citation-ground-check.py --root ."),
        ("R6-gate-quote-audit-root", "python3 corpus/instruments/gate-quote-audit.py --root ."),
        ("R7-routed-defects-root", "python3 corpus/instruments/r44-routed-defects.py --root ."),
        ("R8-capture-binding-pipeline",
         "python3 corpus/instruments/capture-binding-check.py --root . | grep -c records=84"),
    ]
    for name, derive in positives:
        direct_rc, direct_out, _direct_err = run(["/bin/sh", "-c", derive], lane, env=env,
                                                 timeout=a.timeout)
        direct_value = direct_out.strip()
        rc, out, err = probe(work, gate, lane, name.split("-")[0].lower(), derive,
                             direct_value, env)
        admitted = not refused(rc, err)
        if direct_rc == 0:
            value_ok = rc == 0 and ("FIG %s " % name.split("-")[0].lower()) in out and " ok" in out
        else:
            value_ok = rc == 1 and ("FIG %s " % name.split("-")[0].lower()) in out
        record(name, admitted and value_ok,
               "direct_rc=%d gate_rc=%d admitted=%d value_ok=%d"
               % (direct_rc, rc, int(admitted), int(value_ok)))

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
    observed = 0
    if tail:
        try:
            observed = int(tail[-1].split()[1].split("=")[1])
        except (IndexError, ValueError):
            observed = 0
    pin = [ln for ln in out.splitlines() if ln.startswith("selftest pin ")]
    record("selftest", rc == 0 and bool(tail) and observed >= a.min_selftest
           and tail[-1].endswith("failures=0") and not pin,
           "%s rc=%d min=%d" % (tail[-1] if tail else "no-cases-line", rc, a.min_selftest))

    mutbat = os.path.join(lane, "corpus", "instruments", "figure-audit-mutbat.py")
    rc, out, err = run([sys.executable, mutbat, "--instrument", gate], work, env=env,
                       timeout=a.timeout)
    record("mutbat", rc == 0,
           "rc=%d %s" % (rc, (out.strip().splitlines() or ["no-output"])[-1][:120]))

    ledger = os.path.join(lane, "corpus", "instruments", "figure-audit-ledger.json")
    rc, out, err = run([sys.executable, gate, "--ledger", ledger, "--root", lane], lane,
                       env=env, timeout=a.timeout)
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
