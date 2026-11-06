#!/usr/bin/env python3
"""c1-forgeries-r81.py — pre-freeze forgery controls for round-81 C1.

Builds five forgeries of the frozen r81 candidate (selftest replaced by a stub that runs no
assertion, plus a guard: F1 location, F2 self-hash, F3 sibling marker, F4 baseline limb,
F5 all-case FAIL when moved — the round-80 CriticClaims F1-F4 shapes plus one aimed at the
case-matched limb) and scores each under (a) the round-80 counter over the 56 non-neutral
rows of the r81 table and (b) the frozen round-81 counter over the full 59-row table. Each
baseline target sits at <work>/<name>/corpus/instruments/recheck-cwd-census.py with a
SIBLING.marker beside it. Prints one FORGERY line per run.
Usage: c1-forgeries-r81.py --lane DIR --work DIR
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

C1 = ".ufo/waves/round-81/c1"
CASES = ["prefix-census", "result-main", "tmpdir-parent", "scratch-cleanup", "first-line",
         "restoration-only", "both-headers", "relabel-detection", "tmpdir-refusal",
         "prefix-literal", "conform-limbs", "tmpdir-file", "timeout-bucket", "tmpdir-unset",
         "usage-guards", "output-lines", "gate-predicates", "gate-wiring", "gate-regs",
         "gate-consume", "gate-negpolarity", "gate-checkids"]
STUB_TAIL = '    print("selftest cases=22 failures=0")\n    return 0\n\n\ndef _orig_selftest():\n'
GUARDS = {
    "F1-location": (
        '    import os\n'
        '    if os.path.basename(os.path.dirname(os.path.abspath(__file__))) != "instruments":\n'
        '        print("selftest case=location FAIL moved")\n'
        '        print("selftest cases=22 failures=1")\n'
        '        return 1\n'),
    "F2-selfhash": None,
    "F3-sibling": (
        '    import os\n'
        '    if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "SIBLING.marker")):\n'
        '        print("selftest case=fixture FAIL got=absent want=SIBLING.marker")\n'
        '        print("selftest cases=22 failures=1")\n'
        '        return 1\n'),
    "F4-baseline": (
        '    import os\n'
        '    if os.path.basename(os.path.dirname(os.path.abspath(__file__))) != "instruments":\n'
        '        print("selftest case=location FAIL moved")\n'
        '        print("selftest cases=22 failures=0")\n'
        '        return 1\n'
        '    print("selftest case=integrity FAIL got=unchecked want=nothing")\n'),
    "F5-allcases": (
        '    import os\n'
        '    if os.path.basename(os.path.dirname(os.path.abspath(__file__))) != "instruments":\n'
        '        for c in %r:\n'
        '            print("selftest case=%%s FAIL moved" %% c)\n'
        '        print("selftest cases=22 failures=22")\n'
        '        return 1\n' % (CASES,)),
}
SENT = "# ---BODY-HASH-SENTINEL---\n"


def forge(src, name):
    anchor = "def selftest():\n"
    assert src.count(anchor) == 1
    if name == "F2-selfhash":
        guard = ('    import hashlib, os\n'
                 '    raw = open(os.path.abspath(__file__), "rb").read()\n'
                 '    got = hashlib.sha256(raw.split(b"# ---BODY-HASH-SENTINEL---\\n", 1)[1]).hexdigest()\n'
                 '    if got != BODY_SHA:\n'
                 '        print("selftest case=integrity FAIL got=%s" % got)\n'
                 '        print("selftest cases=22 failures=1")\n'
                 '        return 1\n')
        body = src.replace(anchor, anchor + guard + STUB_TAIL, 1)
        first, rest = body.split("\n", 1)
        tail = rest
        sha = hashlib.sha256(tail.encode("utf-8")).hexdigest()
        return first + "\n" + 'BODY_SHA = "%s"\n' % sha + SENT + tail
    return src.replace(anchor, anchor + GUARDS[name] + STUB_TAIL, 1)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args(argv)
    lane = os.path.abspath(a.lane)
    src = open(os.path.join(lane, C1, "recheck-cwd-census.py"), encoding="utf-8").read()
    table = json.load(open(os.path.join(lane, C1, "mutant-table.json"), encoding="utf-8"))
    nonneutral = [r for r in table if r["class"] != "neutral"]
    t56 = os.path.join(a.work, "table-r81-nonneutral.json")
    with open(t56, "w", encoding="utf-8") as fh:
        json.dump(nonneutral, fh)
    for name in sorted(GUARDS):
        home = os.path.join(a.work, name, "corpus", "instruments")
        os.makedirs(home)
        target = os.path.join(home, "recheck-cwd-census.py")
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(forge(src, name))
        open(os.path.join(home, "SIBLING.marker"), "w").close()
        sha = hashlib.sha256(open(target, "rb").read()).hexdigest()
        for counter, tbl in (("r80", t56), ("r81", os.path.join(lane, C1, "mutant-table.json"))):
            mb = os.path.join(lane, ".ufo/waves/round-%s/c1/mutbat.py" % counter[1:])
            wd = os.path.join(a.work, name, "w-" + counter)
            os.makedirs(wd)
            p = subprocess.run([sys.executable, "-B", mb, "--target", target, "--table", tbl,
                                "--expect-cases", "22", "--work", wd],
                               capture_output=True, text=True, cwd=lane)
            summary = [l for l in p.stdout.splitlines() if l.startswith("MUTBAT")]
            verdicts = {}
            for l in p.stdout.splitlines():
                m = re.match(r"MUTANT \S+ verdict=(\S+)", l)
                if m:
                    verdicts[m.group(1)] = verdicts.get(m.group(1), 0) + 1
            print("FORGERY %s counter=%s forgery_sha256=%s rc=%d verdicts=%s %s"
                  % (name, counter, sha, p.returncode, json.dumps(verdicts, sort_keys=True),
                     summary[-1] if summary else "NO-SUMMARY stderr=%r" % p.stderr[-200:]))
        shutil.rmtree(os.path.join(a.work, name), ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
