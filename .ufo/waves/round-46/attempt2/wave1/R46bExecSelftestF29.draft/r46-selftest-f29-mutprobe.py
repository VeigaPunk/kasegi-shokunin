#!/usr/bin/env python3
"""Scratch harness (not committed): apply single-line mutants to the F29 gate and check that
the new selftest reports failures>0 for each (i.e. the mutant is caught)."""
import json
import os
import re
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
SCRATCH = "/fast/scratch/hyaku/kasegi-r46/R46bExecSelftestF29"
SELFTEST = os.path.join(LANE, ".ufo/waves/round-46/attempt2/wave1/R46bExecSelftestF29.draft/r46-selftest-f29.py")
GATE = os.path.join(LANE, "corpus/instruments/r46-f29-gate.py")

MUTANTS = [
    ("H1a-counts-loose", 'if len(rows) != 29 or adm != 29 or dup:', 'if len(rows) < 29 or adm < 29:'),
    ("H1b-raw-loose", 'if len(raw) != 1:', 'if len(raw) < 1:'),
    ("H1c-src-boundary", 're.search(r"\\bS074\\b", f29[0][4])', 're.search(r"S074", f29[0][4])'),
    ("H2a-verified-loose", 'ok_v = any(h == "verified-at: " + VERIFIED_AT for h in head)', 'ok_v = any(h.startswith("verified-at: " + VERIFIED_AT) for h in head)'),
    ("H2b-wordfloor-low", '(12 if sct.startswith("## Falsifiable") else 25)', '(1 if sct.startswith("## Falsifiable") else 5)'),
    ("H2c-need-empty", 'need = {"github-private-vulnerability-reporting.md", "cna-assignment-and-vulnerability-rules.md"}', 'need = set()'),
    ("H3a-cells-loose", 'if len(c) == 11:', 'if len(c) >= 9:'),
    ("H3b-scope-low", 'if len(re.findall(r"\\w+", row[4])) < 8: bad.append("scope-words")', 'if len(re.findall(r"\\w+", row[4])) < 2: bad.append("scope-words")'),
    ("H3c-kind-dead", 'if row[2] != "docs": bad.append("kind")', 'if row[2] != "Docs": bad.append("kind")'),
    ("H4a-manifest-unpinned", 'if sha(open(man, "rb").read()) != PINS["manifest.json"]:', 'if False:'),
    ("H4b-quotes-low", 'oks >= 8 and not miss', 'oks >= 1 and not miss'),
    ("H4c-distinct-dropped", 'and "BROKEN" not in out and distinct', 'and "BROKEN" not in out'),
    ("H5a-span-wide", 'b - a <= 11', 'b - a <= 110'),
    ("H5b-words-wide", 'len(nq.split()) <= 25', 'len(nq.split()) <= 250'),
    ("H5c-pass-low", 'len(passed) >= 4', 'len(passed) >= 1'),
    ("H6a-counts-loose", 'return (len(names) == 66 and len(everything) == 66 and nested == 66 and base_ok and sized and not links,', 'return (len(names) == 66 and base_ok and sized and not links,'),
    ("H6b-pin-dropped", 'base_ok = base_ok and cont == PINS["base-knowledge-content"] and ledger_ok', 'base_ok = base_ok and ledger_ok'),
    ("H6c-size-low", 'os.path.getsize(os.path.join(root, p)) >= 3000', 'os.path.getsize(os.path.join(root, p)) >= 3'),
    ("H7a-verdict-or", 'return p.returncode == 0 and ok_line, "census-rc=%d ok-line=%d" % (p.returncode, int(ok_line))', 'return p.returncode == 0 or ok_line, "census-rc=%d ok-line=%d" % (p.returncode, int(ok_line))'),
    ("H7b-symlink-dead", 'return False, "census-input-is-a-symlink"', 'pass  # mutant H7b'),
    ("H7c-okline-loose", 're.search(r"^\\S+\\tok\\t", p.stdout, re.M)', 're.search(r"^\\S+\\tok", p.stdout, re.M)'),
]

text = open(GATE, encoding="utf-8").read()
rows = []
for mid, old, new in MUTANTS:
    n = text.count(old)
    if n != 1:
        rows.append((mid, "SKIP old-substring-count=%d" % n))
        continue
    d = os.path.join(SCRATCH, "mut", mid)
    shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(os.path.join(LANE, "corpus/instruments"), os.path.join(d, "corpus", "instruments"))
    dst = os.path.join(d, "corpus", "instruments", "r46-f29-gate.py")
    open(dst, "w", encoding="utf-8").write(text.replace(old, new, 1))
    p = subprocess.run([sys.executable, SELFTEST, "--counter", dst, "--work", os.path.join(d, "work")],
                       capture_output=True, text=True, timeout=1800, cwd=LANE)
    m = re.findall(r"failures=(\d+)", p.stdout)
    f = int(m[-1]) if m else -1
    verdict = "caught" if f >= 1 else "uncaught"
    rows.append((mid, "%s mutant_failures=%d" % (verdict, f)))
    if f >= 1:
        for ln in p.stdout.splitlines():
            if ln.startswith("FAIL"):
                print("   " + ln)
    shutil.rmtree(d, ignore_errors=True)
for mid, r in rows:
    print("mutant=%-24s %s" % (mid, r))
print("mutants=%d caught=%d" % (len(rows), sum(1 for _, r in rows if r.startswith("caught"))))
