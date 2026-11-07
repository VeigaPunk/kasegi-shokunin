#!/usr/bin/env python3
"""kasegi round-98 C1 control harness — census-at-rev.py.

Builds a scratch fixture clone of the lane (never the live lane), commits the
candidate instrument and the candidate census there, and runs the frozen
control set. Every fixture declares the reasons it is allowed to fail on, and
the harness prints `ATTRIBUTION pass fixtures=N` (R150).

Controls:
  candidate            the candidate census checked against its own revision -> rc 0
  do-nothing           the base census file (no measured-at line)            -> rc 1 no-measured-at
  tampered-pinned      candidate census with one pinned digit changed        -> rc 1 pinned-mismatch
  stale-rev            candidate census pointing at an older revision        -> rc 1 pinned-mismatch
  no-pinned-line       measured-at present, pinned line removed              -> rc 1 no-pinned-line
  missing-file         a path that does not exist                            -> rc 2 missing-file
  bad-revision         a revision that is not in the fixture repo            -> rc 2 bad-revision
  no-resolve           a revision whose extract has no resolve.py            -> rc 2 no-resolve

Usage:
  python3 -B .ufo/waves/round-98/controls/c1-controls-r98.py \
      --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin --work <scratch> \
      --instrument corpus/instruments/census-at-rev.py --base <rev>
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

CENSUS = "corpus/instruments/citation-survival.md"
INSTR = "corpus/instruments/census-at-rev.py"
STALE_REV = "b06af5e07efbd961a8449f7de6b57eeea62c6bd3"   # round-97 base


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def git(d, *args):
    return sh(["git", "-C", d] + list(args))


def commit(d, msg):
    git(d, "add", "-A")
    env = dict(os.environ, GIT_AUTHOR_DATE="2026-11-07T00:00:00Z",
               GIT_COMMITTER_DATE="2026-11-07T00:00:00Z")
    r = subprocess.run(["git", "-C", d, "-c", "user.name=fixture",
                        "-c", "user.email=fixture@invalid", "commit", "-q", "-m", msg],
                       capture_output=True, text=True, env=env)
    if r.returncode != 0:
        raise SystemExit("fixture commit failed: " + r.stderr)
    top = git(d, "rev-parse", "--show-toplevel").stdout.strip()
    if os.path.realpath(top) != os.path.realpath(d):
        raise SystemExit("fixture root mismatch")
    return git(d, "rev-parse", "HEAD").stdout.strip()


def run_measure(fixture, rev, work):
    r = sh([sys.executable, "-B", os.path.join(fixture, INSTR),
            "--lane", fixture, "--rev", rev, "--work", os.path.join(work, "instwork")])
    out = r.stdout + r.stderr
    reason = "none"
    m = re.search(r"reason=([a-z0-9-]+)", out)
    if m:
        reason = m.group(1)
    return r.returncode, reason, out


def run_check(fixture, census, rev, work):
    r = sh([sys.executable, "-B", os.path.join(fixture, INSTR),
            "--lane", fixture, "--rev", rev, "--check", census,
            "--work", os.path.join(work, "instwork")])
    out = r.stdout + r.stderr
    reason = "none"
    m = re.search(r"reason=([a-z0-9-]+)", out)
    if m:
        reason = m.group(1)
    return r.returncode, reason, out


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--instrument", default=INSTR)
    ap.add_argument("--base", required=True)
    a = ap.parse_args(argv)
    lane = os.path.abspath(a.lane)
    work = os.path.abspath(a.work)
    os.makedirs(work, exist_ok=True)
    fixture = os.path.join(work, "fixture")
    shutil.rmtree(fixture, ignore_errors=True)
    r = sh(["git", "clone", "-q", "--shared", lane, fixture])
    if r.returncode != 0:
        print("C1-CONTROLS-RESULT error reason=clone rc=2")
        return 2
    head = git(fixture, "rev-parse", "HEAD").stdout.strip()
    if head != a.base:
        print("C1-CONTROLS-RESULT error reason=base-mismatch head=%s rc=2" % head)
        return 2

    shutil.copyfile(os.path.join(lane, a.instrument), os.path.join(fixture, INSTR))
    os.chmod(os.path.join(fixture, INSTR), 0o755)
    rev_inst = commit(fixture, "candidate instrument")
    r = sh([sys.executable, "-B", os.path.join(fixture, INSTR), "--lane", fixture,
            "--rev", rev_inst, "--write", os.path.join(fixture, CENSUS),
            "--work", os.path.join(work, "instwork")])
    if r.returncode != 0:
        print("C1-CONTROLS-RESULT error reason=write rc=2")
        print(r.stdout + r.stderr)
        return 2
    rev_cand = commit(fixture, "candidate census")
    cand = os.path.join(fixture, CENSUS)
    with open(cand, encoding="utf-8") as fh:
        cand_text = fh.read()

    # base census (the do-nothing state) and the derived fixtures
    base_census = os.path.join(work, "base-census.md")
    b = subprocess.run(["git", "-C", lane, "show", "%s:%s" % (a.base, CENSUS)],
                       capture_output=True, text=True)
    with open(base_census, "w", encoding="utf-8") as fh:
        fh.write(b.stdout)
    tampered = os.path.join(work, "tampered.md")
    m = re.search(r"^pinned rate \(INTERNAL only; revision-stable\): SKILL (\d+)/", cand_text, re.M)
    with open(tampered, "w", encoding="utf-8") as fh:
        fh.write(cand_text.replace("SKILL %s/" % m.group(1), "SKILL %d/" % (int(m.group(1)) + 1), 1))
    stale = os.path.join(work, "stale.md")
    with open(stale, "w", encoding="utf-8") as fh:
        fh.write(re.sub(r"^measured-at: [0-9a-f]{40}$", "measured-at: " + STALE_REV,
                        cand_text, count=1, flags=re.M))
    nopinned = os.path.join(work, "no-pinned.md")
    with open(nopinned, "w", encoding="utf-8") as fh:
        fh.write(re.sub(r"^pinned rate .*$", "", cand_text, count=1, flags=re.M))

    # a revision with resolve.py deleted
    os.unlink(os.path.join(fixture, "corpus/instruments/resolve.py"))
    rev_noresolve = commit(fixture, "no resolve")

    cases = [
        ("candidate", "check", cand, rev_cand, 0, {"none"}),
        ("do-nothing", "check", base_census, rev_cand, 1, {"no-measured-at"}),
        ("tampered-pinned", "check", tampered, rev_cand, 1, {"pinned-mismatch"}),
        ("stale-rev", "check", stale, rev_cand, 1, {"pinned-mismatch"}),
        ("no-pinned-line", "check", nopinned, rev_cand, 1, {"no-pinned-line"}),
        ("missing-file", "check", os.path.join(work, "absent.md"), rev_cand, 2, {"missing-file"}),
        ("bad-revision", "measure", None, "0" * 40, 2, {"bad-revision"}),
        ("no-resolve", "measure", None, rev_noresolve, 2, {"no-resolve"}),
    ]
    bad = 0
    for name, mode, path, rev, want, declared in cases:
        if mode == "check":
            rc, reason, out = run_check(fixture, path, rev, work)
        else:
            rc, reason, out = run_measure(fixture, rev, work)
        ok = rc == want and reason in declared
        bad += not ok
        print("CONTROL %s rc=%d want=%d %s reason=%s declared=%s" % (
            name, rc, want, "PASS" if ok else "FAIL", reason, ",".join(sorted(declared))))
        if not ok:
            print(out[-1200:])
    print("ATTRIBUTION %s fixtures=%d" % ("pass" if not bad else "fail", len(cases)))
    print("C1-CONTROLS-RESULT %s controls=%d rc=%d" % (
        "pass" if not bad else "fail", len(cases), 0 if not bad else 1))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
