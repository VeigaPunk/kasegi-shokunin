#!/usr/bin/env python3
"""Census-freshness gate (round-50 C1): the committed citation-survival census of
record must be byte-identical to what resolve.py generates over the current tree.

Usage:
  python corpus/instruments/census-freshness-check.py <lane-repo-root>
  python corpus/instruments/census-freshness-check.py --selftest [--lane-root DIR]

Why (round-49 lesson, mistake 1): the committed census of record described a tree
the lane no longer had — "Scope: ... (50 files)" and a lane rate of 134/1480 while
the live instrument run read 202 files and 4771 distinct citations. Nothing
failed: the census was stale, and the round quoted it anyway. This gate makes
that state exit 1.

Contract:
  * exit 0 and one line `CENSUS-FRESH=ok`  — both committed census files
    (citation-survival.md, citation-survival.tsv) are byte-identical to the
    files `resolve.py` writes over the current tree;
  * exit 1 and `CENSUS-FRESH=stale`        — any byte differs (stale OR tampered;
    the gate does not distinguish motive, only bytes);
  * exit 2                                 — missing instrument/census, or the
    resolver run itself failed. Fail-closed: an unmeasurable tree is never ok.
  * the gate always restores the census bytes it found: a run changes nothing on
    success, and on failure the committed (stale/tampered) bytes are put back so
    the evidence of record is preserved, not silently repaired by the checker.

Determinism note: the census embeds the lane root path it was generated from, so
the committed census is bound to one host path; moving the lane re-baselines it
(recorded round-50 debt, owner operator). `--selftest` builds three disposable
fixture lanes (fresh / stale / tampered) around a copy of the lane's own
resolve.py and prints one `case=<name> want=<exit> got=<exit> verdict=<pass|fail>`
line per case plus `selftest cases=3 failures=F`; it exits 0 only when F=0.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

CENSUS_MD = os.path.join("corpus", "instruments", "citation-survival.md")
CENSUS_TSV = os.path.join("corpus", "instruments", "citation-survival.tsv")
RESOLVER = os.path.join("corpus", "instruments", "resolve.py")


def snapshot(root):
    out = {}
    for rel in (CENSUS_MD, CENSUS_TSV):
        path = os.path.join(root, rel)
        with open(path, "rb") as fh:
            out[rel] = fh.read()
    return out


def restore(root, snap):
    for rel, data in snap.items():
        with open(os.path.join(root, rel), "wb") as fh:
            fh.write(data)


def run_gate(root):
    """Run the gate against one lane root. Returns (exit, message)."""
    resolver = os.path.join(root, RESOLVER)
    for rel in (CENSUS_MD, CENSUS_TSV, RESOLVER):
        if not os.path.isfile(os.path.join(root, rel)):
            return 2, "CENSUS-FRESH=error reason=missing %s" % rel
    try:
        snap = snapshot(root)
    except OSError as exc:
        return 2, "CENSUS-FRESH=error reason=%s" % exc
    proc = subprocess.run([sys.executable, resolver, root], cwd=root,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        restore(root, snap)
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()
        detail = tail[-1][:160] if tail else "resolver exited %d" % proc.returncode
        return 2, "CENSUS-FRESH=error reason=resolver-failed: %s" % detail
    try:
        regen = snapshot(root)
    finally:
        restore(root, snap)
    diffs = [rel for rel in (CENSUS_MD, CENSUS_TSV) if regen[rel] != snap[rel]]
    if not diffs:
        return 0, "CENSUS-FRESH=ok files=2"
    which = "+".join(os.path.basename(r) for r in diffs)
    return 1, ("CENSUS-FRESH=stale files=%s "
               "(committed bytes differ from what resolve.py generates over the current tree; "
               "regenerate the census or repair the tree)" % which)


def build_fixture(lane_root, dest):
    """A miniature lane: SKILL.md + two corpus files + the lane's own resolve.py."""
    inst = os.path.join(dest, "corpus", "instruments")
    os.makedirs(inst)
    os.makedirs(os.path.join(dest, "corpus", "knowledge"))
    shutil.copyfile(os.path.join(lane_root, RESOLVER), os.path.join(inst, "resolve.py"))
    with open(os.path.join(dest, "SKILL.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# fixture lane\n\nRun `corpus/knowledge/a.md` and then `ops/rank.mjs:46`.\n")
    with open(os.path.join(dest, "corpus", "knowledge", "a.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# A\n\nCites `SKILL.md` and `corpus/knowledge/a.md:1`.\n")
    proc = subprocess.run([sys.executable, os.path.join(inst, "resolve.py"), dest],
                          cwd=dest, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        raise SystemExit("fixture census generation failed: %s"
                         % (proc.stderr or proc.stdout).strip()[:200])


def selftest(lane_root):
    cases = []
    tmp = tempfile.mkdtemp(prefix="census-fresh-")
    try:
        # case 1 — fresh: census generated over the current tree, gate must say ok.
        fresh = os.path.join(tmp, "fresh")
        os.makedirs(fresh)
        build_fixture(lane_root, fresh)
        code, msg = run_gate(fresh)
        cases.append(("fresh", 0, code, msg))
        # case 2 — stale: tree grows after the census was taken.
        stale = os.path.join(tmp, "stale")
        os.makedirs(stale)
        build_fixture(lane_root, stale)
        with open(os.path.join(stale, "corpus", "knowledge", "b.md"), "w",
                  encoding="utf-8", newline="\n") as fh:
            fh.write("# B\n\nCites `evidence/new-file.md:3` which the census never saw.\n")
        code, msg = run_gate(stale)
        cases.append(("stale", 1, code, msg))
        # case 3 — tampered: the committed census bytes are edited in place.
        tamp = os.path.join(tmp, "tampered")
        os.makedirs(tamp)
        build_fixture(lane_root, tamp)
        md = os.path.join(tamp, CENSUS_MD)
        with open(md, "r", encoding="utf-8") as fh:
            text = fh.read()
        marker = None
        for line in text.splitlines():
            if "distinct path-like citations" in line:
                marker = line
                break
        if marker is None:
            raise SystemExit("tamper fixture: marker line not found in census")
        text = text.replace(marker, marker.replace("citations", "citations TAMPERED-EDIT"), 1)
        with open(md, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
        code, msg = run_gate(tamp)
        cases.append(("tampered", 1, code, msg))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    failures = 0
    for name, want, got, msg in cases:
        ok = want == got
        failures += 0 if ok else 1
        print("case=%s want=%d got=%d verdict=%s  # %s"
              % (name, want, got, "pass" if ok else "FAIL", msg))
    print("selftest cases=%d failures=%d" % (len(cases), failures))
    return 0 if failures == 0 else 1


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("root", nargs="?", help="lane repo root")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--lane-root", dest="lane_root", default=None,
                    help="lane root whose resolve.py the selftest copies (default: this file's dir/../..)")
    args = ap.parse_args(argv)
    if args.selftest:
        lane_root = args.lane_root or os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return selftest(lane_root)
    if not args.root:
        ap.error("lane repo root required (or --selftest)")
    code, msg = run_gate(args.root)
    print(msg)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
