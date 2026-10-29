#!/usr/bin/env python3
"""r46-mutbat.py — round-46 (attempt 2) mutation-battery runner (depth:verifiability work), v1.1.

WHAT IT DOES
    Applies a frozen set of single-edit mutants to scratch copies of the round-46 claim
    counters (`r46-c1-gate.py`, `r46-c2-gate.py`, `r46-f29-gate.py`), runs the tree's own
    selftest against each mutant, and grades each mutant:

        caught      the selftest reports failures>0 under the mutant while the unmutated
                    counter reads failures=0 (baseline must be clean);
        equivalent  the mutant id carries a committed proof in --equivalent (JSON: id -> path)
                    arguing the mutated clause cannot change any verdict on any input;
        uncaught    neither (a hole in the selftest's coverage).

    Each mutant is a (id, old-substring, new-substring) triple; the edit is asserted to
    occur EXACTLY ONCE in the counter copy, so a drifted counter fails loudly instead of
    mutating the wrong line. Mutant copies live under --work (TMPDIR honoured); the lane
    tree is only read. Never runs git; stdlib only.

    v1.1 adds the f29 counter (round-46 C2): the frozen F29_MUTANTS table (21 triples
    against `r46-f29-gate.py`, the R50 pre-freeze mutant set of
    `.ufo/waves/round-46/attempt2/controls/f29-r50-receipt.txt`) and `--counter f29`.
    The f29 grader is the f29 selftest when one is present — the wave-1 draft at
    `.ufo/waves/round-46/attempt2/wave1/R46bExecSelftestF29.draft/r46-selftest-f29.py`,
    else the committed `corpus/instruments/r46-selftest-f29.py` — invoked with the mutated
    gate through `--counter` (or with a tree whose gate is the mutant, when the selftest
    grades a tree instead of a counter file); when neither selftest is present the grader
    falls back to the R50 fixture corpus (`controls/f29-fixture.py` +
    `controls/f29-defects.py`): the pristine and the mutated gate are both run over every
    fixture tree and a mutant is caught when it changes a verdict. Grading, classification
    and output lines are identical for all three counters.

USAGE
    python3 corpus/instruments/r46-mutbat.py --root TREE --pure PURE_EXPORT \
        --work DIR [--counter c1|c2|f29|both|all] [--jobs N] [--equivalent MAP.json] [--list]

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

# --- F29 mutant table: r46-f29-gate.py, 3 per limb H1-H7 ---------------------------
# The R50 pre-freeze pass (.ufo/waves/round-46/attempt2/controls/f29-r50-receipt.txt)
# names these 21 mutants and records, per mutant, the defect tree that flips its limb.
# The triples below are the content-addressed single edits of r46-f29-gate.py that realise
# those clauses; every old substring occurs EXACTLY ONCE in the gate, so a drifted gate
# fails loudly instead of mutating the wrong line.
F29_MUTANTS = [
    ("H1a-counts-loose",    "if len(rows) != 29 or adm != 29 or dup:",                        "if len(rows) < 29 or adm < 29 or dup:"),
    ("H1b-raw-loose",       "if len(raw) != 1:",                                              "if len(raw) > 1:"),
    ("H1c-src-boundary",    "re.search(r\"\\bS074\\b\", f29[0][4])",                           "re.search(r\"S074\", f29[0][4])"),
    ("H2a-verified-loose",  "ok_v = any(h == \"verified-at: \" + VERIFIED_AT for h in head)",  "ok_v = any(h.startswith(\"verified-at: \" + VERIFIED_AT) for h in head)"),
    ("H2b-wordfloor-low",   "(12 if sct.startswith(\"## Falsifiable\") else 25)",              "(1 if sct.startswith(\"## Falsifiable\") else 5)"),
    ("H2c-need-empty",      "need = {\"github-private-vulnerability-reporting.md\", \"cna-assignment-and-vulnerability-rules.md\"}", "need = set()"),
    ("H3a-cells-loose",     "if len(c) == 11:",                                               "if len(c) >= 9:"),
    ("H3b-scope-low",       "if len(re.findall(r\"\\w+\", row[4])) < 8: bad.append(\"scope-words\")", "if len(re.findall(r\"\\w+\", row[4])) < 2: bad.append(\"scope-words\")"),
    ("H3c-kind-dead",       "if row[2] != \"docs\": bad.append(\"kind\")",                     "if row[2] not in (\"docs\", \"Docs\"): bad.append(\"kind\")"),
    ("H4a-manifest-unpinned","if sha(open(man, \"rb\").read()) != PINS[\"manifest.json\"]:",    "if False:"),
    ("H4b-quotes-low",      "oks >= 8 and not miss",                                          "oks >= 1 and not miss"),
    ("H4c-distinct-dropped","and \"BROKEN\" not in out and distinct",                         "and \"BROKEN\" not in out"),
    ("H5a-span-wide",       "b - a <= 11",                                                    "b - a <= 110"),
    ("H5b-words-wide",      "len(nq.split()) <= 25",                                          "len(nq.split()) <= 250"),
    ("H5c-pass-low",        "len(passed) >= 4",                                               "len(passed) >= 1"),
    ("H6a-counts-loose",    "len(names) == 66 and len(everything) == 66 and nested == 66",      "len(names) == 66 and len(everything) >= 66 and nested >= 66"),
    ("H6b-pin-dropped",     "base_ok = base_ok and cont == PINS[\"base-knowledge-content\"] and ledger_ok", "base_ok = base_ok and ledger_ok"),
    ("H6c-size-low",        "os.path.getsize(os.path.join(root, p)) >= 3000",                  "os.path.getsize(os.path.join(root, p)) >= 3"),
    ("H7a-verdict-or",      "p.returncode == 0 and ok_line",                                  "p.returncode == 0 or ok_line"),
    ("H7b-symlink-dead",    "return False, \"census-input-is-a-symlink\"",                      "pass  # mutant H7b"),
    ("H7c-okline-loose",    "re.search(r\"^\\S+\\tok\\t\", p.stdout, re.M)",                   "re.search(r\"^\\S+\\tok\", p.stdout, re.M)"),
]

COUNTER = {"c1": ("r46-c1-gate.py", C1_MUTANTS, "r46-counters-selftest-c1.py"),
           "c2": ("r46-c2-gate.py", C2_MUTANTS, "r46-counters-selftest-c2.py"),
           "f29": ("r46-f29-gate.py", F29_MUTANTS, "r46-selftest-f29.py")}

# --- f29 grader wiring -----------------------------------------------------------
F29_DRAFT_SELFTEST = ("/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/"
                       "attempt2/wave1/R46bExecSelftestF29.draft/r46-selftest-f29.py")
F29_CONTROLS_REL = os.path.join(".ufo", "waves", "round-46", "attempt2", "controls")
F29_CONTROLS_ABS = ("/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/"
                    "attempt2/controls")
F29_FIXTURE_MODES = ("positive", "junk", "fabricated")
F29_DEFECTS = ("duprow", "fencedf29", "vjunk", "thinsection", "badnames", "row9cells",
               "thinscope", "kindcase", "manws", "fewquotes", "dupquote", "widespan",
               "longquote", "fewspans", "nestedmd", "entrymutant", "symlink")


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


# --- f29 grader: the selftest (preferred) or the R50 fixture corpus (fallback) -----
F29_DRAFT_SELFTEST = ("/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/"
                       "attempt2/wave1/R46bExecSelftestF29.draft/r46-selftest-f29.py")
F29_CONTROLS_REL = os.path.join(".ufo", "waves", "round-46", "attempt2", "controls")
F29_CONTROLS_ABS = ("/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/"
                    "attempt2/controls")
F29_FIXTURE_MODES = ("positive", "junk", "fabricated")
F29_DEFECTS = ("duprow", "fencedf29", "vjunk", "thinsection", "badnames", "row9cells",
               "thinscope", "kindcase", "manws", "fewquotes", "dupquote", "widespan",
               "longquote", "fewspans", "nestedmd", "entrymutant", "symlink")


def f29_find_selftest(tree: str) -> str | None:
    for p in (os.path.join(tree, "corpus/instruments", COUNTER["f29"][2]), F29_DRAFT_SELFTEST):
        if p and os.path.isfile(p):
            return p
    return None


def f29_find_controls(tree: str) -> str | None:
    lane_root = os.path.dirname(os.path.dirname(INSTRUMENTS))
    for c in (os.path.join(lane_root, F29_CONTROLS_REL), F29_CONTROLS_ABS):
        if os.path.isfile(os.path.join(c, "f29-fixture.py")):
            return c
    return None


def f29_selftest_flags(selftest: str) -> set[str]:
    p = subprocess.run([sys.executable, "-I", selftest, "--help"], capture_output=True, text=True, timeout=300)
    return set(re.findall(r"--[a-z0-9][a-z0-9-]*", p.stdout + p.stderr))


def f29_run_selftest(tree: str, selftest: str, counter_path: str | None, flags: set[str],
                      pure: str, work: str, jobs: int) -> tuple[int, str]:
    cmd = [sys.executable, "-I", selftest]
    if counter_path and "--counter" in flags:
        cmd += ["--counter", counter_path]
    if counter_path and "--counter" not in flags:
        # the selftest grades a tree instead of a counter file: hand it the tree copy whose
        # gate is the mutant copy (built by the caller).
        cmd += ["--root", counter_path]
    if "--pure" in flags:
        cmd += ["--pure", pure]
    if "--work" in flags:
        cmd += ["--work", work]
    if "--jobs" in flags:
        cmd += ["--jobs", str(jobs)]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=1800, cwd=tree)
    m = re.findall(r"failures=(\d+)", p.stdout)
    return (int(m[-1]) if m else -1), p.stdout[-2000:]


def f29_build_fixture_corpus(tree: str, work: str, controls: str) -> dict[str, str]:
    """Build the R50 fixture corpus: the three entry modes and the 17 per-limb defect trees.

    The fixture builders read a lane that has the F29 landing STRIPPED (28 frontier rows,
    no F29 entry file) and write their own F29 row and entry, so the corpus is built from a
    `view` of the tree under test with those two bytes removed.
    """
    view = os.path.join(work, "f29-view")
    trees_dir = os.path.join(work, "f29-trees")
    shutil.rmtree(view, ignore_errors=True)
    shutil.rmtree(trees_dir, ignore_errors=True)
    os.makedirs(os.path.join(view, "corpus"), exist_ok=True)
    os.makedirs(trees_dir, exist_ok=True)
    rd = open(os.path.join(tree, "corpus/README.md"), encoding="utf-8").read()
    rd = "".join(ln for ln in rd.splitlines(True) if not re.match(r"^\| F29 \|", ln))
    open(os.path.join(view, "corpus/README.md"), "w", encoding="utf-8").write(rd)
    shutil.copytree(os.path.join(tree, "corpus/knowledge"), os.path.join(view, "corpus/knowledge"))
    snap = os.path.join(view, "corpus/source-snapshots/round-46-a2")
    os.makedirs(snap, exist_ok=True)
    for f in ("S074.txt", "manifest.json"):
        shutil.copy(os.path.join(tree, "corpus/source-snapshots/round-46-a2", f), os.path.join(snap, f))

    trees: dict[str, str] = {}
    for mode in F29_FIXTURE_MODES:
        d = os.path.join(trees_dir, mode)
        subprocess.run([sys.executable, os.path.join(controls, "f29-fixture.py"), "--mode", mode,
                        "--dir", d, "--lane", view], check=True, timeout=900)
        trees[mode] = d
    for defect in F29_DEFECTS:
        d = os.path.join(trees_dir, defect)
        subprocess.run([sys.executable, os.path.join(controls, "f29-defects.py"), "--defect", defect,
                        "--dir", d, "--lane", view], check=True, timeout=900)
        trees[defect] = d
    # src0740: the receipt's pair-3 tree (sources cell S0740); controls/f29-defects.py does
    # not ship it, so it is derived from the positive tree here.
    d = os.path.join(trees_dir, "src0740")
    shutil.copytree(trees["positive"], d, symlinks=True)
    p = os.path.join(d, "corpus/README.md")
    t = open(p, encoding="utf-8").read()
    row = [ln for ln in t.splitlines() if ln.startswith("| F29 |")][0]
    open(p, "w", encoding="utf-8").write(t.replace(row, row.replace("| S074 |", "| S0740 |"), 1))
    trees["src0740"] = d
    return trees


def f29_gate_verdicts(gate: str, tree: str) -> dict[str, int]:
    p = subprocess.run([sys.executable, gate, "--root", tree], capture_output=True, text=True, timeout=900)
    out: dict[str, int] = {}
    for m in re.finditer(r"^gate (H\d) pass=(\d) ", p.stdout, re.M):
        out[m.group(1)] = int(m.group(2))
    return out


def grade_f29(tree: str, pure: str, work: str, jobs: int, eq: dict[str, str]) -> tuple[int, int, int, int, list[str]]:
    """Grade the 21 f29 mutants. Returns (caught, equivalent, uncaught, baseline_failures, lines)."""
    lines: list[str] = []
    src_counter = os.path.join(tree, "corpus/instruments", COUNTER["f29"][0])
    if not os.path.isfile(src_counter):
        lines.append("mutbat counter=f29 GATE-MISSING %s" % src_counter)
        return 0, 0, 0, 1, lines

    selftest = f29_find_selftest(tree)
    controls = f29_find_controls(tree)
    flags: set[str] = set()
    trees: dict[str, str] = {}
    baseline_trees: dict[str, dict[str, int]] = {}
    grader = ""
    if selftest:
        flags = f29_selftest_flags(selftest)
    if selftest and ("--counter" in flags or "--root" in flags or "--lane" in flags):
        grader = "selftest"
    elif controls:
        grader = "fixture"
        trees = f29_build_fixture_corpus(tree, work, controls)
        for name in sorted(trees):
            baseline_trees[name] = f29_gate_verdicts(src_counter, trees[name])
    else:
        lines.append("mutbat counter=f29 NO-GRADER (no selftest, no fixture controls)")
        return 0, 0, 0, 1, lines

    base_failures = 0
    if grader == "selftest":
        base_failures, _tail = f29_run_selftest(tree, selftest, None, flags, pure,
                                                 os.path.join(work, "base-f29"), jobs)
    else:
        # baseline expectations: the positive tree is green, every other fixture tree trips
        # at least one limb.
        for name in sorted(baseline_trees):
            v = baseline_trees[name]
            green = len(v) == 7 and all(v[k] for k in v)
            if name == "positive":
                if not green:
                    base_failures += 1
            elif green:
                base_failures += 1

    if base_failures != 0:
        lines.append("mutbat counter=f29 BASELINE-DIRTY baseline_failures=%d" % base_failures)
        return 0, 0, 0, base_failures, lines

    caught = equivalent = uncaught = 0
    for mid, old, new in F29_MUTANTS:
        mdir = tempfile.mkdtemp(prefix="mutbat-%s-" % mid.split("-")[0], dir=work)
        try:
            dst = apply_mutant(src_counter, (mid, old, new), mdir, tree)
            if grader == "selftest":
                if "--counter" in flags:
                    mf, _ = f29_run_selftest(tree, selftest, dst, flags, pure,
                                             os.path.join(mdir, "run"), jobs)
                else:
                    # the selftest grades a tree: put the mutant gate into a tree copy and
                    # hand the copy over.
                    tcopy = os.path.join(mdir, "tree")
                    os.makedirs(os.path.join(tcopy, "corpus"), exist_ok=True)
                    shutil.copytree(os.path.join(tree, "corpus"), os.path.join(tcopy, "corpus"), symlinks=True)
                    shutil.copy(dst, os.path.join(tcopy, "corpus/instruments", COUNTER["f29"][0]))
                    mf, _ = f29_run_selftest(tree, selftest, tcopy, flags, pure,
                                             os.path.join(mdir, "run"), jobs)
            else:
                mf = 0
                for name in sorted(baseline_trees):
                    v = f29_gate_verdicts(dst, trees[name])
                    if v != baseline_trees[name]:
                        mf += 1
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
        lines.append("mutant=%s baseline_failures=0 mutant_failures=%d verdict=%s" % (mid, mf, verdict))
    return caught, equivalent, uncaught, base_failures, lines


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", required=True, help="tree whose counters and selftests are graded")
    ap.add_argument("--pure", required=True, help="PURE base export passed through to the selftests")
    ap.add_argument("--work", required=True, help="scratch dir (mutant copies and selftest scratch live here)")
    ap.add_argument("--counter", default="both", choices=["c1", "c2", "f29", "both", "all"])
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--equivalent", default=None, help="JSON file mapping mutant id -> proof path")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args(argv)

    if a.list:
        for which in ("c1", "c2", "f29"):
            for mid, old, new in COUNTER[which][1]:
                print("%s %s | %s => %s" % (which, mid, old[:60], new[:60]))
        return 0

    eq = {}
    if a.equivalent:
        eq = json.load(open(a.equivalent, encoding="utf-8"))
    os.makedirs(a.work, exist_ok=True)
    bad = 0
    for which in ("c1", "c2"):
        if a.counter not in ("both", "all", which):
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
    if a.counter in ("f29", "all"):
        caught, equivalent, uncaught, base_failures, lines = grade_f29(a.root, a.pure, a.work, a.jobs, eq)
        for ln in lines:
            print(ln)
        if base_failures == 0:
            print("mutbat counter=f29 mutants=%d caught=%d equivalent=%d uncaught=%d baseline_failures=0" %
                  (len(F29_MUTANTS), caught, equivalent, uncaught))
        if uncaught or base_failures:
            bad += 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
