#!/usr/bin/env python3
"""Round-45 freeze controls: score the frozen C1/C2 counters on cheap do-nothing,
marker-only, junk-row and fabricated-quote trees BEFORE any wave seat runs.

Usage: freeze-controls.py --base-export DIR --lane DIR --work DIR
  --base-export  git-archive export of the frozen base (dc5bb8c6e31efc4a6650819df85e79b72fd64bcd)
  --lane         the lane checkout holding the counters and snapshots
  --work         scratch dir (under $HYAKU_SCRATCH/kasegi-r45/...)
Prints one `control <name> counter=<C1|C2> <counter summary line> expect=RED got=RED|GREEN`.
Exit 0 only when every control is RED (the counter rejects it).
"""
import argparse, os, re, shutil, subprocess, sys


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def cp(src, dst):
    shutil.copytree(src, dst, symlinks=True)


def append(path, text):
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(text)


def c1(lane, root, base):
    rc, out = run([sys.executable, os.path.join(lane, "corpus/instruments/r45-routed-defects.py"),
                   "--root", root, "--baseline", base])
    return rc, out.strip().splitlines()[-1]


def c2(lane, root):
    rc, out = run([sys.executable, os.path.join(lane, "corpus/instruments/r45-c2-gate.py"), "--root", root])
    return rc, out.strip().splitlines()[-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-export", required=True)
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    rows = []

    # 1. do-nothing: the pristine base export
    rows.append(("do-nothing-base", "C1", c1(a.lane, a.base_export, a.base_export)))
    rows.append(("do-nothing-base", "C2", c2(a.lane, a.base_export)))

    # 2. C1 marker-only: prose markers for every limb, no artifacts behind them
    m = os.path.join(a.work, "c1-marker-only")
    shutil.rmtree(m, ignore_errors=True)
    cp(a.base_export, m)
    append(os.path.join(m, "corpus/lessons/round-44.md"),
           "\nCorrection (round 45): S072 supersedes S070; the directory body is readable, 10029 characters.\n")
    append(os.path.join(m, "corpus/QUALITY.md"),
           "\n## Round-45 additions\n\n| id | criterion | grounded in |\n|---|---|---|\n"
           "| R47 | do-nothing control before data. enforced-by: `corpus/instruments/nothing.py` | corpus/lessons/round-44.md |\n"
           "| R48 | presence-only predicates. enforced-by: `corpus/instruments/nothing.py` | corpus/lessons/round-44.md |\n"
           "| R49 | capture method parity for reject. enforced-by: `corpus/instruments/nothing.py` | corpus/lessons/round-44.md |\n")
    append(os.path.join(m, "SKILL.md"),
           "\n## Round-45 Gates & probes registry addition\n\n| name | a | b | c | d | e | f | g |\n|---|---|---|---|---|---|---|---|\n"
           "| r44-frontier-count.py | 1 | 2 | 3 | 4 | 5 | 6 | 7 |\n| r44-routed-defects.py | 1 | 2 | 3 | 4 | 5 | 6 | 7 |\n"
           "| wave-registry.py | 1 | 2 | 3 | 4 | 5 | 6 | 7 |\n")
    append(os.path.join(m, "corpus/instruments/README.md"), "\n| `r44-frontier-count.py` | registered |\n")
    ctl = os.path.join(m, ".ufo/waves/round-44/controls")
    append(os.path.join(ctl, "final-attempt3-refiled.txt"), "selftest cases=20 failures=0\nexit=0\n")
    rows.append(("c1-marker-only", "C1", c1(a.lane, m, a.base_export)))

    # 3. C2 junk-row: frontier row, registry row, empty entry, count restored — no source work
    j = os.path.join(a.work, "c2-junk-row")
    shutil.rmtree(j, ignore_errors=True)
    cp(a.base_export, j)
    append(os.path.join(j, "corpus/README.md"),
           "\n| id | topic | status | entry | sources | next |\n|---|---|---|---|---|---|\n"
           "| F27 | junk | admitted | `knowledge/junk-entry.md` | S071 | none |\n")
    with open(os.path.join(j, "corpus/knowledge/junk-entry.md"), "w", encoding="utf-8") as fh:
        fh.write("# junk\n\nsource: S071 — https://docs.kernel.org/process/security-bugs.html\n"
                 "verified-at: 2026-10-28\nrecheck: true\n")
    rows.append(("c2-junk-row", "C2", c2(a.lane, j)))

    # 4. C2 fabricated quotes: snapshot + manifest are genuine, entry quotes text the source does not hold
    f = os.path.join(a.work, "c2-fabricated-quote")
    shutil.copytree(j, f, symlinks=True)
    shutil.copytree(os.path.join(a.lane, "corpus/source-snapshots/round-45"),
                    os.path.join(f, "corpus/source-snapshots/round-45"), dirs_exist_ok=True)
    with open(os.path.join(f, "corpus/knowledge/junk-entry.md"), "w", encoding="utf-8") as fh:
        fh.write("# fabricated\n\nsource: S071 — https://docs.kernel.org/process/security-bugs.html\n"
                 "verified-at: 2026-10-28\nrecheck: true\n\n"
                 "“embargoes last up to 7 calendar days for every reporter” (`S071.txt:310`)\n"
                 "“AI-found bugs treat it as public by default” (`S071.txt:95`)\n"
                 "“Binary-only executables are not accepted for kernels” (`S071.txt:39`)\n"
                 "“a bug that cannot be reproduced, it is not exploitable” (`S071.txt:42`)\n")
    rows.append(("c2-fabricated-quote", "C2", c2(a.lane, f)))

    bad = 0
    for name, ctr, (rc, line) in rows:
        got = "RED" if rc != 0 else "GREEN"
        bad += 1 if got != "RED" else 0
        print(f"control {name} counter={ctr} {line} expect=RED got={got}")
    print(f"controls total={len(rows)} red={len(rows) - bad} green={bad}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
