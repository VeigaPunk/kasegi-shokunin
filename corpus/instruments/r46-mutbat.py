#!/usr/bin/env python3
"""r46-mutbat.py — round-46 (attempt 2) mutation-battery runner (depth:verifiability work).

WHAT IT DOES
    Applies a frozen set of single-edit mutants to scratch copies of the round-46 claim
    counters (`r46-c1-gate.py`, `r46-c2-gate.py`), runs the tree's own selftest against
    each mutant, and grades each mutant:

        caught      the selftest reports failures>0 under the mutant while the unmutated
                    counter reads failures=0 (baseline must be clean);
        equivalent  the mutant id carries a committed proof in --equivalent (JSON: id -> path)
                    arguing the mutated clause cannot change any verdict on any input;
        uncaught    neither (a hole in the selftest's coverage).

    Each mutant is a (id, old-substring, new-substring) triple; the edit is asserted to
    occur EXACTLY ONCE in the counter copy, so a drifted counter fails loudly instead of
    mutating the wrong line. Mutant copies live under --work (TMPDIR honoured); the lane
    tree is only read. Never runs git; stdlib only.

USAGE
    python3 corpus/instruments/r46-mutbat.py --root TREE --pure PURE_EXPORT \
        --work DIR [--counter c1|c2|both] [--jobs N] [--equivalent MAP.json] [--list]

OUTPUT
    one `mutant=<id> baseline_failures=<b> mutant_failures=<m> verdict=<v>` line per mutant, then
    `mutbat counter=<c> mutants=<n> caught=<k> equivalent=<e> uncaught=<u> baseline_failures=<b> exit=0|1`
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

SELF = os.path.realpath(__file__)
INSTRUMENTS = os.path.dirname(SELF)

# --- C1 mutant table: r46-c1-gate.py, one single-line edit each -----------------
C1_MUTANTS = [
    ("M01-L1-target-24",     "TARGET_GATED = 22",                                              "TARGET_GATED = 24"),
    ("M02-L1-broken-ignored","<= TARGET_GATED and not broken and len(ct) >= len(cb)",          "<= TARGET_GATED and len(ct) >= len(cb)"),
    ("M03-L1-floor-dropped", "and len(ct) >= len(cb)",                                         ""),
    ("M04-L2-one-reground",  "len(reg) >= MIN_REGROUNDED",                                     "len(reg) >= 1"),
    ("M05-L3-shape-loose",   "(?:[ \\t]+#.*)?$",                                               ".*$"),
    ("M06-L3-home-dropped",  "or HOME_RE.search(CD_RE.sub(\"\", ct[e][\"line\"], count=1))",   ""),
    ("M07-L3-home-no-abs",   "re.compile(r\"(?:~/|\\$HOME|\\$\\{HOME\\}|/home/)\")",           "re.compile(r\"(?:~/|\\$HOME|\\$\\{HOME\\})\")"),
    ("M08-L4-bytes-dropped", "and read(bp) == read(tp)):",                                     "):"),
    ("M09-L4-planted-dropped","if p.returncode != 0 or planted:",                              "if p.returncode != 0:"),
    ("M10-L4-symlink-ok",    "if os.path.islink(fp) or not os.path.isfile(fp)",                "if not os.path.isfile(fp)"),
    ("M11-L5-prefix-flip",   "if t[:len(b)] != b or",                                          "if t[:len(b)] == b or"),
    ("M12-L5-restore-dropped","or rest_ok != [want]:",                                         ":"),
    ("M13-L6-control-dropped","if c.returncode != 0:",                                         "if False:"),
    ("M14-L6-exit-ignored",  "if p.returncode == 0 or red != [r[0]]:",                         "if red != [r[0]]:"),
    ("M15-L7-always-true",   "res.append((\"L7\", not bad7,",                                  "res.append((\"L7\", True,"),
    ("M16-min-rows-5",       "MIN_ROWS = 6",                                                   "MIN_ROWS = 5"),
    ("M17-min-token-1",      "MIN_TOKEN = 8",                                                  "MIN_TOKEN = 1"),
    ("M18-anchor-dirs-wide", "ANCHOR_DIRS = (\"corpus/instruments/\", \"corpus/source-snapshots/\")",
                              "ANCHOR_DIRS = (\"corpus/instruments/\", \"corpus/source-snapshots/\", \"corpus/knowledge/\")"),
    ("M19-L2-eq-relaxed",    "and len(gt) == len(gb) - len(reg) and not (gt - gb)",            "and len(gt) <= len(gb)"),
    ("M20-syntax-ignored",   "if subprocess.run([\"bash\", \"-n\", \"-c\", line], capture_output=True).returncode != 0:",
                              "if False:"),
]

# --- C2 mutant table: r46-c2-gate.py, >= 3 single-line edits per gate -----------
C2_MUTANTS = [
    ("G1a-counts-loose",   "if len(rows) != 28 or adm != 28 or dup:",                          "if len(rows) < 28 or adm < 28:"),
    ("G1b-path-dropped",   "if f27[2] != \"admitted\" or p is None:",                          "if f27[2] != \"admitted\":"),
    ("G1c-src-boundary",   "re.search(r\"\\bS073\\b\", f27[4])",                               "re.search(r\"S073\", f27[4])"),
    ("G2a-verified-prefix","ok_v = any(h == \"verified-at: 2026-10-28\" for h in head)",       "ok_v = any(h.startswith(\"verified-at: 2026-10-28\") for h in head)"),
    ("G2b-wordfloor-low",  "(12 if sct.startswith(\"## Falsifiable\") else 25)",               "(1 if sct.startswith(\"## Falsifiable\") else 5)"),
    ("G2c-need-empty",     "need = {\"linux-kernel-security-bugs-reporting-process.md\", \"ai-assisted-finding-validation.md\"}", "need = set()"),
    ("G3a-cells-loose",    "if len(c) == 11:",                                                 "if len(c) >= 9:"),
    ("G3b-scope-words-low","if len(re.findall(r\"\\w+\", row[4])) < 8: bad.append(\"scope-words\")", "if len(re.findall(r\"\\w+\", row[4])) < 2: bad.append(\"scope-words\")"),
    ("G3c-kind-dead",      "if row[2] != \"docs\": bad.append(\"kind\")",                      "if row[2] != \"Docs\": bad.append(\"kind\")"),
    ("G4a-manifest-unpinned","if sha(open(man, \"rb\").read()) != PINS[\"manifest.json\"]:",   "if False:"),
    ("G4b-quotes-low",     "oks >= 8 and not miss",                                            "oks >= 1 and not miss"),
    ("G4c-distinct-dropped","and \"BROKEN\" not in out and distinct",                          "and \"BROKEN\" not in out"),
    ("G5a-span-wide",      "b - a <= 11",                                                      "b - a <= 110"),
    ("G5b-words-wide",     "len(nq.split()) <= 25",                                            "len(nq.split()) <= 250"),
    ("G5c-pass-low",       "len(passed) >= 4",                                                 "len(passed) >= 1"),
    ("G6a-guards-dead",    "if links or not grown:",                                           "if False:"),
    ("G6b-integrity-loose","return (len(names) == 65 and len(everything) == 65 and nested == 65 and base_ok and sized),", "return (len(names) == 65 and base_ok and sized),"),
    ("G6c-size-low",       "os.path.getsize(os.path.join(root, p)) >= 3000",                   "os.path.getsize(os.path.join(root, p)) >= 3"),
    ("G7a-verdict-or",     "return rc == 0 and ok_line, f\"census-rc={rc} ok-line={int(ok_line)}\"", "return rc == 0 or ok_line, f\"census-rc={rc} ok-line={int(ok_line)}\""),
    ("G7b-symlink-dead",   "return False, \"census-input-is-a-symlink\"",                      "pass  # mutant G7b"),
    ("G7c-okline-loose",   "re.search(r\"^\\S+\\tok\\t\", out, re.M)",                         "re.search(r\"^\\S+\\tok\", out, re.M)"),
]

COUNTER = {"c1": ("r46-c1-gate.py", C1_MUTANTS, "r46-counters-selftest-c1.py"),
           "c2": ("r46-c2-gate.py", C2_MUTANTS, "r46-counters-selftest-c2.py")}


def run_selftest(tree: str, which: str, counter_path: str | None, pure: str, work: str, jobs: int) -> tuple[int, str]:
    st = os.path.join(tree, "corpus/instruments", COUNTER[which][2])
    cmd = [sys.executable, "-I", st]
    if counter_path:
        cmd += ["--counter", counter_path]
    if which == "c1":
        cmd += ["--pure", pure, "--work", work, "--jobs", str(jobs)]
    else:
        cmd += ["--pure", pure]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=1800, cwd=tree)
    m = re.findall(r"failures=(\d+)", p.stdout)
    return (int(m[-1]) if m else -1), p.stdout[-2000:]


def apply_mutant(src_counter: str, triple: tuple[str, str, str], dst_dir: str, tree: str) -> str:
    mid, old, new = triple
    text = open(src_counter, encoding="utf-8").read()
    n = text.count(old)
    if n != 1:
        raise SystemExit("mutant=%s old-substring occurs %d times (expected 1) — battery vs counter drift" % (mid, n))
    # copy the tree's whole instruments dir so the counter's TOOL_LANE-style resolution stays intact
    dst_inst = os.path.join(dst_dir, "corpus", "instruments")
    shutil.copytree(os.path.join(tree, "corpus", "instruments"), dst_inst, symlinks=True)
    dst_counter = os.path.join(dst_inst, os.path.basename(src_counter))
    open(dst_counter, "w", encoding="utf-8").write(text.replace(old, new, 1))
    return dst_counter


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", required=True, help="tree whose counters and selftests are graded")
    ap.add_argument("--pure", required=True, help="PURE base export passed through to the selftests")
    ap.add_argument("--work", required=True, help="scratch dir (mutant copies and selftest scratch live here)")
    ap.add_argument("--counter", default="both", choices=["c1", "c2", "both"])
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--equivalent", default=None, help="JSON file mapping mutant id -> proof path")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args(argv)

    if a.list:
        for which in ("c1", "c2"):
            for mid, old, new in COUNTER[which][1]:
                print("%s %s | %s => %s" % (which, mid, old[:60], new[:60]))
        return 0

    eq = {}
    if a.equivalent:
        eq = json.load(open(a.equivalent, encoding="utf-8"))
    os.makedirs(a.work, exist_ok=True)
    bad = 0
    for which in ("c1", "c2"):
        if a.counter != "both" and a.counter != which:
            continue
        cname, mutants, _st = COUNTER[which]
        src_counter = os.path.join(a.root, "corpus/instruments", cname)
        baseline, tail = run_selftest(a.root, which, None, a.pure, os.path.join(a.work, "base-" + which), a.jobs)
        if baseline != 0:
            print("mutbat counter=%s BASELINE-DIRTY baseline_failures=%d" % (which, baseline))
            print(tail)
            bad += 1
            continue
        caught = equivalent = uncaught = 0
        for mid, old, new in mutants:
            mdir = tempfile.mkdtemp(prefix="mutbat-%s-" % mid.split("-")[0], dir=a.work)
            try:
                dst = apply_mutant(src_counter, (mid, old, new), mdir, a.root)
                mf, _ = run_selftest(a.root, which, dst, a.pure, os.path.join(mdir, "run"), a.jobs)
            finally:
                shutil.rmtree(mdir, ignore_errors=True)
            if mf >= 1:
                caught += 1
                verdict = "caught"
            elif mid in eq and os.path.isfile(eq[mid]):
                equivalent += 1
                verdict = "equivalent"
            else:
                uncaught += 1
                verdict = "uncaught"
            print("mutant=%s baseline_failures=0 mutant_failures=%d verdict=%s" % (mid, mf, verdict))
        print("mutbat counter=%s mutants=%d caught=%d equivalent=%d uncaught=%d baseline_failures=0" %
              (which, len(mutants), caught, equivalent, uncaught))
        if uncaught:
            bad += 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
