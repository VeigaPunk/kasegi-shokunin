#!/usr/bin/env python3
"""Round-69 C1 counter: the derive gate must refuse the program-execution and write residuals
that the round-68 wave measured open (R69-a..d, `.ufo/waves/round-68/w1/{CriticC1,RevengerC1}.md`).

Frozen predicate (claims.json): on the gate named by --gate, `VERIFY measurements=13 failures=0`
and process exit 0.  The thirteen measurements are

  P1 sort-compress-prefix-equals   `sort --compress-prog=<comp> -S 1K big.txt | head -n 1`
  P2 sort-compress-prefix-space    `sort --co <comp> -S 1K big.txt | head -n 1`
  P3 sort-output-prefix            `sort --outp=w3.txt big.txt | head -n 1`
  P4 sort-bundled-short-o          `sort -uo w4.txt big.txt | head -n 1`
  P5 git-show-commit-form          `git show HEAD | head -n 1`        (default textconv on a commit diff)
  P6 git-show-message-search       `git show ':/fixture' | head -n 1` (`:/` resolves to a commit)
  P7 git-cat-file-textconv         `git cat-file --textconv HEAD:big.txt | head -n 1`
  P8 git-cat-file-filters          `git cat-file --filters HEAD:f.txt | head -n 1` (smudge filter)
      each: refused at parse time (exit 2, stderr reason=derive-not-read-only), its program marker
      gains no line and its named output file does not exist.
  9  read-only-controls-admitted   nine legitimate read-only derives (sort, cat, grep, cut, git show
                                    blob and tree form, git cat-file -p/-t, git ls-tree) still run and
                                    re-derive their exact value (positive controls: a blanket refusal
                                    fails here).
  10 selftest                      `<gate> --selftest` exits 0 with `selftest cases=86 failures=0`.
  11 mutbat                        the committed exact-once mutant battery exits 0 against <gate>.
  12 real-ledger                   the committed lane ledger re-derives `figures=35 ok=35 stale=0`.
  13 no-write-side-effect          fixture and repo trees (including .git) byte-identical before
                                    and after every run, and all three program markers at 0.

Pointed at the BASE gate bytes (round-68 tip `656272cf`) this same counter is the do-nothing
control: every probe P1..P8 is admitted, P1/P2/P5/P6/P7/P8 execute their program, P3/P4 write
their file, the selftest pins 77 cases, and the write-side-effect measurement fails.

Usage:
  python3 .ufo/waves/round-69/controls/c1-probe-run-r69.py --gate PATH --work DIR [--lane DIR] [--mode M]

--work must be an owned scratch directory under $HYAKU_SCRATCH (the counter builds fixtures only
inside it and never writes elsewhere).  Host binaries matter: results are for the PATH `sort`,
`git` and `python3` the counter runs with; the receipt header records their versions.
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
EXPECTED_SELFTEST = "selftest cases=86 failures=0"


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


def write_exec(path, body):
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    os.chmod(path, 0o755)


def build_fixture(work):
    fixture = os.path.join(work, "fixture")
    repo = os.path.join(work, "repo")
    for d in (fixture, repo):
        if os.path.isdir(d):
            shutil.rmtree(d)
        os.makedirs(d)
    with open(os.path.join(fixture, "big.txt"), "w", encoding="utf-8") as f:
        f.write("".join("%07d\n" % i for i in range(BIG_LINES)))
    with open(os.path.join(repo, "big.txt"), "w", encoding="utf-8") as f:
        f.write("x" * 1000 + "\n")
    with open(os.path.join(repo, "f.txt"), "w", encoding="utf-8") as f:
        f.write("filtered\n")
    comp = os.path.join(work, "compressor.sh")
    driver = os.path.join(work, "textconv.sh")
    smudge = os.path.join(work, "smudge.sh")
    write_exec(comp, '#!/bin/sh\necho run >> "$COMP_MARK"\nexec gzip -c\n')
    write_exec(driver, '#!/bin/sh\necho run >> "$TC_MARK"\nexec cat "$1"\n')
    write_exec(smudge, '#!/bin/sh\necho run >> "$SM_MARK"\nexec cat\n')
    git = ["git", "-C", repo]
    rc, out, err = run(git + ["init", "-q", "."], work)
    if rc != 0:
        raise SystemExit("fixture git init failed rc=%d %s" % (rc, err))
    rc, out, _ = run(git + ["rev-parse", "--show-toplevel"], work)
    if rc != 0 or os.path.realpath(out.strip()) != os.path.realpath(repo):
        raise SystemExit("fixture toplevel mismatch: %r" % out.strip())
    identity = ["-c", "user.email=fixture@shokunin.local", "-c", "user.name=fixture"]
    for argv in (git + ["config", "diff.mydriver.textconv", driver],
                 git + ["config", "diff.mydriver.binary", "false"],
                 git + ["config", "filter.myfilter.smudge", smudge],
                 git + ["config", "filter.myfilter.clean", "cat"]):
        rc, _, err = run(argv, work)
        if rc != 0:
            raise SystemExit("fixture git config failed rc=%d %s" % (rc, err))
    with open(os.path.join(repo, ".gitattributes"), "w", encoding="utf-8") as f:
        f.write("big.txt diff=mydriver\nf.txt filter=myfilter\n")
    for argv in (git + ["add", "-A"], git + identity + ["commit", "-qm", "fixture commit"]):
        rc, _, err = run(argv, work)
        if rc != 0:
            raise SystemExit("fixture git %s failed rc=%d %s" % (argv[-1], rc, err))
    return fixture, repo, comp, driver, smudge


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
    ap = argparse.ArgumentParser(description="kasegi r69 C1 program-execution class counter")
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

    fixture, repo, comp, driver, smudge = build_fixture(work)
    marks = {k: os.path.join(work, "marker." + k) for k in ("compress", "textconv", "smudge")}
    for p in marks.values():
        open(p, "w").close()
    env = dict(os.environ)
    env["COMP_MARK"] = marks["compress"]
    env["TC_MARK"] = marks["textconv"]
    env["SM_MARK"] = marks["smudge"]
    env["TMPDIR"] = work
    env["HYAKU_SCRATCH"] = work

    before = tree_state(fixture) + tree_state(repo)
    rows = []

    def record(name, ok, detail):
        rows.append((name, ok, detail))
        print("MEASURE %s %s %s" % (name, "ok" if ok else "FAIL", detail))

    probes = [
        ("sort-compress-prefix-equals", fixture,
         "sort --compress-prog=%s -S 1K big.txt | head -n 1" % comp, BIG_WANT, "compress", None),
        ("sort-compress-prefix-space", fixture,
         "sort --co %s -S 1K big.txt | head -n 1" % comp, BIG_WANT, "compress", None),
        ("sort-output-prefix", fixture,
         "sort --outp=w3.txt big.txt | head -n 1", BIG_WANT, None, "w3.txt"),
        ("sort-bundled-short-o", fixture,
         "sort -uo w4.txt big.txt | head -n 1", BIG_WANT, None, "w4.txt"),
        ("git-show-commit-form", repo,
         "git show HEAD | head -n 1", "commit", "textconv", None),
        ("git-show-message-search", repo,
         "git show ':/fixture' | head -n 1", "commit", "textconv", None),
        ("git-cat-file-textconv", repo,
         "git cat-file --textconv HEAD:big.txt | head -n 1", TEXT_WANT, "textconv", None),
        ("git-cat-file-filters", repo,
         "git cat-file --filters HEAD:f.txt | head -n 1", "filtered", "smudge", None),
    ]
    for i, (name, root, derive, want, mark, outfile) in enumerate(probes, 1):
        start = {k: marker_lines(p) for k, p in marks.items()}
        rc, out, err = probe(work, gate, root, "p%d" % i, derive, want, env)
        ran = (marker_lines(marks[mark]) - start[mark]) if mark else 0
        wrote = os.path.exists(os.path.join(root, outfile)) if outfile else False
        refused = rc == 2 and "reason=derive-not-read-only" in err
        record("P%d-%s" % (i, name), refused and ran == 0 and not wrote,
               "rc=%d refused=%d marker_runs=%d wrote=%d" % (rc, int(refused), ran, int(wrote)))

    controls = [
        ("sort -r big.txt | head -n 1", fixture, "%07d" % (BIG_LINES - 1)),
        ("cat big.txt | wc -l", fixture, str(BIG_LINES)),
        ("grep -c 0000001 big.txt", fixture, "1"),
        ("cut -c1-3 big.txt | head -n 1", fixture, "000"),
        ("git show HEAD:big.txt | head -n 1", repo, TEXT_WANT),
        ("git show HEAD: | head -n 1", repo, "tree HEAD:"),
        ("git cat-file -p HEAD:f.txt", repo, "filtered"),
        ("git cat-file -t HEAD", repo, "commit"),
        ("git ls-tree --name-only HEAD | head -n 1", repo, ".gitattributes"),
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
    record("mutbat", rc == 0, "rc=%d %s" % (rc, (out.strip().splitlines() or ["no-output"])[-1][:120]))

    ledger = os.path.join(lane, "corpus", "instruments", "figure-audit-ledger.json")
    rc, out, err = run([sys.executable, gate, "--ledger", ledger, "--root", lane], lane, env=env,
                       timeout=a.timeout)
    line = [ln for ln in out.splitlines() if ln.startswith("FIGURE-AUDIT")]
    record("real-ledger", rc == 0 and bool(line) and "figures=35 ok=35 stale=0" in line[-1],
           "%s rc=%d" % (line[-1] if line else "no-audit-line", rc))

    after = tree_state(fixture) + tree_state(repo)
    runs = sum(marker_lines(p) for p in marks.values())
    record("no-write-side-effect", before == after and runs == 0,
           "fixture_changed=%d marker_runs=%d" % (0 if before == after else 1, runs))

    failures = sum(1 for _, ok, _ in rows if not ok)
    print("VERIFY measurements=%d failures=%d gate_sha256=%s mode=%s"
          % (len(rows), failures, sha256_file(gate), a.mode))
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
